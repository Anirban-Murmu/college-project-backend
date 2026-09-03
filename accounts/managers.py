from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,tc,middle_name="",gender=None,image=None,password=None):

        if not email:
            raise ValueError("User must have an email address.")

        if not first_name:
            raise ValueError("User must have a first name.")

        if not last_name:
            raise ValueError("User must have a last name.")

        if not tc:
            raise ValueError(
                "You must accept Terms and Conditions."
            )

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            image=image,
            tc=tc,
        )

        # Hash password
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self,email,first_name,last_name,password=None,tc=True,middle_name="",gender=None):

        user = self.create_user(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            password=password,
            tc=tc,
        )

        user.is_admin = True
        user.is_active = True

        user.save(using=self._db)

        return user