from django.db.models.signals import post_save, post_delete
from .models import Review, Movie
from django.dispatch import receiver
from django.db.models import Avg
import logging


@receiver([post_save, post_delete], sender=Review)
def update_overall_rating(instance, **kwargs):
    """
    Update the average rating for a movie when a review is created, updated, or deleted.
    """
    review = Review.objects.filter(movie=instance.movie).aggregate(
        Avg("rating")
    )
    movie = instance.movie
    movie.average_rating = (
        review["rating__avg"] if review["rating__avg"] is not None else 0
    )

    try:
        movie.save()
    except Exception as e:
        logger = logging.getLogger("custom")
        logger.error(f"Failed to update movie rating: {str(e)}")
