class FileManagementService:
    @staticmethod
    def upload_movie(instance, filename) -> str:
        return f"movies/{instance.id}.mp4"
