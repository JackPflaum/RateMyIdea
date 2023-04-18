from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Idea, Comment, Rating
from users.models import Author
from django.db.models import Sum, Avg
from .forms import NewIdeaForm, CommentForm, RatingForm
from django.views import View
from django.contrib.auth.decorators import login_required


def home(request):
    """home page showing most recent ideas posted by users"""
    # annotate query_set method allows you to add new fields to an instance in a query_set based on values
    # of related fields or calculations on those fields.
    # average_rating is a new field added to the Idea instance query_set that 
    # idea_rating is the related name, meaning the reverse relationship from Idea to Rating.
    # idea_rating__rating is a field lookup that traverses the reverse relationship and accesses the
    # rating field of Rating model.
    ideas_list = Idea.objects.all().annotate(average_rating=Avg('idea_rating__rating'))

    # ideas per page from Idea model
    paginator = Paginator(ideas_list, 20)

    # retrieve page number
    page = request.GET.get('page')
    ideas = paginator.get_page(page)
    context = {'ideas': ideas}
    return render(request, 'home.html', context)


class IdeaView(View):
    template_name = 'idea.html'

    def get_average_rating(self, idea):
        """get average rating for an idea"""
        ratings = Rating.objects.filter(idea=idea)
        # aggregate function used to perform calcs on database records. Takes one or more arguments.
        # returns dictionary containing results of calcs.
        # rating__sum is the key used to access the sum of the 'rating' values from the dictionary.
        total_ratings = ratings.aggregate(Sum('rating'))['rating__sum'] or 0
        number_of_ratings = ratings.count() or 0
        return total_ratings / number_of_ratings
    
    def get(self, request, slug):
        """ get idea, user comments and forms for displaying to user"""
        comment_form = CommentForm()
        rating_form = RatingForm()
        idea = Idea.objects.get(slug=slug)
        rating = self.get_average_rating(idea)

        # double underscore __ is used to perform lookups that span relationships
        # idea__slug means that we are transversing the 'idea' relationship and filtering the slug field of the 'Idea' model
        comments = Comment.objects.filter(idea__slug=slug).order_by('date_commented')
        context = {'comment_form': comment_form, 'rating_form': rating_form,
                   'idea': idea, 'rating': rating, 'comments': comments}
        return render(request, self.template_name, context)
    

    @login_required
    def post(self, request, slug):
        """handle Post request for user comment or rating of idea.
        Redirect to login screen  if not logged in."""
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)

        # allow for updating user rating if they've already rated. if rating exits then update.
        # I used filter() because it returns an empty query_set whereas get() raises 
        # a DoesNotExist exception that needs to be handled.
        idea = Idea.object.get(slug=slug)
        rating_exists = Rating.objects.filter(idea=idea, author=request.user).first()

        if rating_exists and rating_form.is_valid():
            # update existing rating
            rating_exists.rating = rating_form.cleaned_data['rating']
            rating_exists.save()
        if comment_form.is_valid() and not rating_form.is_valid():
            # only save comment form
            comment = comment_form.save(commit=False)
            comment.idea = Idea.objects.get(slug=slug)
            comment.author = request.user
            comment.save()
        elif rating_form.is_valid() and not comment_form.is_valid():
            # only save users rating form
            rating = rating_form.save(commit=False)
            rating.idea = Idea.objects.get(slug=slug)
            rating.author = request.user
            rating.save()

        return redirect('ideas:idea')


@login_required
def new_idea(request):
    """new idea form for users to write their idea"""
    if request.method == 'POST':
        form = NewIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)    # don't save to the database yet
            idea.author = request.user    # save the current user in the author field of the Idea model
            idea.save()    # save users idea to the database
            return redirect('ideas:home')
    else:
        form = NewIdeaForm()
    return render(request, 'new_idea.html', {'form': form})


def about(request):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def author(request, slug):
    """author profile page showing previous ideas that have been posted"""
    author = Author.objects.get(slug=slug)
    ideas = Idea.objects.filter(author=author.user)
    number_of_ideas_published = Idea.objects.filter(author=author.user).count()
    context = {'author': author, 'ideas': ideas, 'number_of_ideas_published': number_of_ideas_published}
    return render(request, 'author.html', context)