from django.db import models, IntegrityError
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Q


# 1. Profile
class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    bio = models.TextField()

    email = models.EmailField(unique=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


# 2. Skill
class Skill(models.Model):
    CATEGORY_CHOICES = (
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("tools", "Tools"),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["category", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "category"], name="unique_skill")
        ]


# 3. Technology
class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Technologies"  # ✅ Added plural name


# 4. Tag
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# 5. Project
class Project(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, db_index=True)

    description = models.TextField()

    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)

    technologies = models.ManyToManyField(
        Technology, blank=True, related_name="projects"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PUBLISHED, db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)

    objects = models.Manager()  # default
    active_objects = ActiveManager()  # filtered

    def save(self, *args, **kwargs):
        self.title = self.title.strip()

        # ✅ Safe Slug Logic: check existence before saving
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Optional validation control
        if kwargs.pop("clean", True):
            self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        github = (self.github_link or "").strip()
        live = (self.live_link or "").strip()

        if not github and not live:
            raise ValidationError("At least one valid link is required.")

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~Q(github_link="") | ~Q(live_link=""),
                name="project_link_required",
            )
        ]


# 6. Project Images
class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    # ✅ Enforced Images: removed blank=True, null=True
    image = models.ImageField(upload_to="projects/")
    alt_text = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # ✅ Improved __str__
        return f"Image for {self.project.title}"

    class Meta:
        ordering = ["-created_at"]


# 7. Contact
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        # ✅ Improved __str__: Makes it clear who the message is from and what it's about
        return f"From {self.email} - {self.subject or 'No Subject'}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email", "-created_at"])]
