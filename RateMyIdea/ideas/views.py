from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Idea, Comment, Rating
from users.models import Author
from django.db.models import Sum, Avg, Count
from ideas.forms import NewIdeaForm, CommentForm, RatingForm
from users.forms import UpdateImageForm
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseForbidden
from django.core.files.storage import default_storage


def get_number_of_votes(ideas):
    """get the number of users who rated each idea"""
    number_of_votes = []
    for idea in ideas:
        rating_query_set = Rating.objects.filter(idea=idea).aggregate(votes=Count('rating'))
        number_of_votes.append(rating_query_set['votes'])
    return number_of_votes

def get_number_of_comments(ideas):
    """get the number of user comments for each idea"""
    number_of_comments = []
    for idea in ideas:
        comment_query_set = Comment.objects.filter(idea=idea).aggregate(comments=Count('comment'))
        number_of_comments.append(comment_query_set['comments'])
    return number_of_comments

def get_author_context(author):
    """get the author/user information for profile page"""
    ideas = Idea.objects.filter(author=author.user)

    # number of ideas the user has published
    number_of_ideas_published = ideas.count()

    context = {'author': author, 'number_of_ideas_published': number_of_ideas_published}
    return context


def home(request):
    """home page showing most recent ideas posted by users"""
    # Get the selected sorting option from the request
    sort_option = request.GET.get('sort', 'latest')  # default to 'latest' if not specified

    # Defined a dictionary to map sorting options to corresponding order_by arguments
    sorting_options = {
        'latest': '-date_posted',
        'highest_rated': '-average_rating',
        'lowest_rated': 'average_rating',
        'not_rated_yet': 'date_posted',  # Change this to your desired default order
    }

    # annotate query_set method allows you to add new fields to an instance in a query_set based on values
    # of related fields or calculations on those fields.
    # average_rating is a new field added to the Idea instance query_set 
    # idea_rating is the related name, meaning the reverse relationship from Idea to Rating.
    # idea_rating__rating is a field lookup that traverses the reverse relationship and accesses the
    # rating field of Rating model.
    ideas_list = Idea.objects.all().annotate(average_rating=Avg('idea_rating__rating')).order_by(sorting_options[sort_option])
                                             
    # ideas per page from Idea model
    paginator = Paginator(ideas_list, 2)

    # retrieve page number
    page = request.GET.get('page')
    ideas = paginator.get_page(page)
    # add ideas to page variable specifically for pagination
    pages = ideas

    # convert to list for easier access in template with combined_data_set
    ideas_list = list(ideas)

    number_of_votes = get_number_of_votes(ideas_list)

    number_of_comments = get_number_of_comments(ideas_list)

    # combine data into one set for easier access in template
    combined_data_set = zip(ideas_list, number_of_votes, number_of_comments)

    form = NewIdeaForm()
    context = {'ideas': combined_data_set, 'pages': pages, 'form': form, 'sort_option': sort_option}
    return render(request, 'home.html', context)


@method_decorator(login_required, name="post")
class IdeaView(TemplateView):
    model = Idea
    template_name = 'idea.html'

    def get_average_rating(self, idea):
        """get average rating for an idea"""
        ratings = Rating.objects.filter(idea=idea)
        # aggregate function used to perform calcs on database records. Takes one or more arguments.
        # returns dictionary containing results of calcs.
        # rating__sum is the key used to access the sum of the 'rating' values from the dictionary.
        total_ratings = ratings.aggregate(Sum('rating'))['rating__sum'] or 0
        number_of_ratings = ratings.count() or 0
        if number_of_ratings > 0:
            return total_ratings/number_of_ratings
        else:
            return None
        
    def get_context_data(self, **kwargs):
        # call corresponding method of parent class and updating context dict. with data defined in get_context_data() method
        context = super().get_context_data(**kwargs)
        # add additional data to context dictionary that is available to all when accessing this method
        context['user'] = self.request.user
        context['rating_form'] = RatingForm()
        context['comment_form'] = CommentForm()

        idea = Idea.objects.get(slug=self.kwargs['slug'])    # self.kwargs is captured from the URL pattern

        # get the number of comments for the idea
        comments_count = Comment.objects.filter(idea=idea).count()
        context['comments_count'] = comments_count

        # if the user is logged in then get the value that they rated the idea
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(idea=idea, author=self.request.user).first()
            user_rating_value = user_rating.rating if user_rating else None
            context['user_rating_value'] = user_rating_value
        return context
    
    def get(self, request, slug):
        """ get idea, user comments and forms for displaying to user"""
        idea = Idea.objects.get(slug=slug)
        rating = self.get_average_rating(idea)

        # double underscore __ is used to perform lookups that span relationships
        # idea__slug means that we are transversing the 'idea' relationship and filtering the slug field of the 'Idea' model
        comments = Comment.objects.filter(idea__slug=slug).order_by('date_commented')
        context = {'idea': idea, 'rating': rating, 'comments': comments}
        context.update(self.get_context_data(**context))
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        """handle Post request for user comment or rating of idea.
        Redirect to login screen  if not logged in."""
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)

        # allow for updating user rating if they've already rated. if rating exists then update.
        # I used filter() because it returns an empty query_set whereas get() raises 
        # a DoesNotExist exception that needs to be handled.
        idea = Idea.objects.get(slug=slug)
        rating_exists = Rating.objects.filter(idea=idea, author=self.request.user).first()

        if rating_form.is_valid():
            if rating_exists:
                # update existing rating
                rating_exists.rating = rating_form.cleaned_data['rating']
                rating_exists.idea = idea
                rating_exists.author = self.request.user
                rating_exists.save()
                messages.success(request, 'You have updated your rating of this idea', extra_tags='alert-success')
            else:
                # create new rating
                rating = rating_form.save(commit=False)
                rating.idea = idea
                rating.author = self.request.user
                rating.save()
                messages.success(request, 'You have successfully rated this idea', extra_tags='alert-success')
        elif comment_form.is_valid() and not rating_form.is_valid():
            # only save comment form
            comment = comment_form.save(commit=False)
            comment.idea = idea
            comment.author = self.request.user
            comment.save()

        rating = self.get_average_rating(idea)        

        comments = Comment.objects.filter(idea__slug=slug).order_by('date_commented')
        context = {'idea': idea, 'rating': rating, 'comments': comments}
        context.update(self.get_context_data(**context))
        return render(request, self.template_name, context)


@login_required
def new_idea(request):
    """new idea form for users to write their idea"""
    if request.method == 'POST':
        form = NewIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)    # don't save to the database yet
            idea.author = request.user    # save the current user in the author field of the Idea model
            idea.save()    # save users idea to the database
            messages.success(request, 'New Idea has been posted', extra_tags='alert-success')
            return redirect('ideas:home')
    else:
        form = NewIdeaForm()
        return render(request, 'new_idea.html', {'form': form})


def author(request, slug):
    """author profile page showing previous ideas that have been posted"""
    # get author and their ideas
    author = get_object_or_404(Author, slug=slug)
    ideas = Idea.objects.filter(author=author.user).annotate(average_rating=Avg('idea_rating__rating')).order_by('-date_posted')

    ideas_list = list(ideas)
    
    # get number of user votes for each idea
    number_of_votes = get_number_of_votes(ideas)

    # get number of comments for each idea
    number_of_comments = get_number_of_comments(ideas)

    # combine data into one set for easier access in template
    combined_data_set = zip(ideas_list, number_of_votes, number_of_comments)

    # number of ideas the user has published
    number_of_ideas_published = ideas.count()

    context = {'author': author, 'ideas': combined_data_set, 'number_of_ideas_published': number_of_ideas_published}
    return render(request, 'profile_page.html', context)


@login_required
def edit_profile(request, slug):
    """update author profile with the ability to change avatar and about info"""
    author = get_object_or_404(Author, slug=slug)
    form = UpdateImageForm()
    context = {'form': form}
    context.update(get_author_context(author))
    return render(request, 'edit_profile.html', context)


@login_required
def update_profile_image(request, user_id):
    """allow users to update their profile image"""
    # check user has permission to update image
    if request.user.id == user_id:
        if request.method == 'POST':
            form = UpdateImageForm(request.POST, request.FILES)
            # check if an image file has been uploaded
            if form.is_valid() and 'image' in request.FILES:
                author = get_object_or_404(Author, slug=request.user.username)

                # delete old image before updating with new image
                if author.image:
                    default_storage.delete(author.image.path)

                author.image = form.cleaned_data.get('image')
                author.save()
                return redirect('ideas:author', slug=request.user.username)
            else:
                messages.warning(request, "Invalid upload. Please try again with different image")
                return redirect('ideas:edit_profile', slug=request.user.username)
        else:
            messages.warning(request, "Something went wrong when updating image. Please try again.")
            return redirect('ideas:author', slug=request.user.username)
    else:
        return HttpResponseForbidden("You do not have permission to perform this action")


def about_author(request, slug):
    """information about this user/author"""
    author = get_object_or_404(Author, slug=slug)
    context = get_author_context(author)
    return render(request, 'profile_about_page.html', context)


@login_required
def profile_security(request, slug):
    """allows user to change their password and template gives user access to delete their account"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)    # keep user logged in
            messages.success(request, "Your password has been updated")
            return redirect('ideas:author', slug=request.user.username)
    else:
        form = PasswordChangeForm(request.user)
        author = get_object_or_404(Author, slug=slug)
        context = {'form': form}
        context.update(get_author_context(author))
    return render(request, 'profile_security.html', context)


@login_required
def delete_account(request):
    """users can delete their account permanently"""
    if request.method == 'POST':
        # logout before deleting account
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('ideas:home')
    else:
        messages.warning(request, "Something went wrong. Please try again.")
        return redirect('ideas:profile_security', slug=request.user.username)


@login_required
def delete_idea(request, idea_slug, author_slug):
    """users can delete their ideas that they have posted"""
    if request.method == 'POST':
        users_idea = get_object_or_404(Idea, slug=idea_slug)
        # confirm the author of the idea is the same as the logged in user
        if author_slug == request.user.username:
            users_idea.delete()
            return redirect('ideas:author', author_slug)
        else:
            messages.warning(request, "You don't have permission to delete this idea")
            return redirect('ideas:author', author_slug)
