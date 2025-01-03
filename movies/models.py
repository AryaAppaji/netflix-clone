from django.db import models
from users.models import CustomUser
from .services.file_management_service import FileManagementService


# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "genres"

    def __str__(self):
        return self.name


# Movie Model
class Movie(models.Model):
    name = models.CharField(max_length=30)
    release_year = models.IntegerField()
    description = models.TextField()
    average_rating = models.FloatField(default=0, blank=True, null=True)
    genres = models.ManyToManyField(
        "Genre", through="MovieGenre", db_index=True
    )
    file = models.FileField(
        upload_to=FileManagementService.upload_movie,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies"

    def __str__(self):
        return self.name


# Explicit Pivot Table (Movie-Genre Relationship)
class MovieGenre(models.Model):
    movie = models.ForeignKey(
        Movie,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="movie_genres",
    )
    genre = models.ForeignKey(
        Genre,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="genre_movies",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movie_genre"
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "genre"], name="unique_movie_genre"
            )  # Modern approach to unique constraint
        ]

    def __str__(self):
        return f"{self.movie.name} - {self.genre.name}"


# Review Model
class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    movie = models.ForeignKey(
        Movie,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="movie_reviews",
    )  # Changed related_name
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.movie.name} - {self.rating}"
