📚 Course Registration System
This project is a Course Registration System built using Django, created for a web programming class. It allows students to register for courses, view their registered and completed courses, and view available courses. It also includes an admin interface for managing courses and student registrations.

Note: screenshots of project in screenshots folder.

Features
🧑‍🎓 Student Features
🔐 User Authentication: Students can log in or create an account.
📄 Profile Page: Displays student's information, registered courses, and completed courses.
📋 Available Courses: Shows courses available for registration based on the completion of prerequisites.
📚 Courses Page: Lists all courses with details, but students cannot register from this page.

🧑‍💼 Admin Features
📝 Manage Courses: Add, edit, and delete courses.
🧑‍🎓 Manage Students: Add, edit, and delete student information.
🗂️ Manage Registrations: Add, edit, and delete student course registrations.

🧭 Navigation Bar
🏠 Home: Navigate to the homepage.
📚 Courses: View the list of all courses and their details.
👤 Username Textbox: Displays the logged-in user's username.
🚪 Logout: Log out from the system.

💻 Installation
1.Clone the repository:
  `git clone https://github.com/momen-Ha/course-registration-system.git`

2.Go to the project directory:
  `cd course-registration-system`

3.Install the required dependencies:
  `pip install -r requirements.txt`

4.Apply migrations:
  `python manage.py migrate`

5.Create a superuser for accessing the admin page:
  `python manage.py createsuperuser`

6.Run the server:
  `python manage.py runserver`


