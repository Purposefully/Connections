# Connections

### *Guided learning app facilitating math instructional routines:*  
> Which One Doesn’t Belong?   
> What do you notice?  What do you wonder?  
> Connecting Representations
___

## Table of Contents
* [Background](#Background)
* [Features](#Features)
* [Technologies Used](#Technologies-Used)
* [Screenshots](#Screenshots)
* [Functionality](#Functionality)
* [Design](#Design)
* [Running Locally](#Running-Locally)

___

## Background
While teaching algebra, I often used the following math instructional routines in my lessons to prompt student thinking and communication and sense-making:
* [Which One Doesn't Belong?](https://wodb.ca/)
* [What do you notice?  What do you wonder?](https://www.youtube.com/watch?v=a-Fth6sOaRA)
* [Connecting Representations](https://curriculum.newvisions.org/math/course/getting-started/instructional-routine-connecting-representations/#:~:text=Connecting%20Representations%20has%20these%20five%20main%20parts%3A%201,Study%20Connections%204%20Create%20a%20Representation%205%20Meta-Reflection)

When Covid-19 sent us all home to distance teach and learn, I wished for a way to at least partially replicate these powerful routines online.  This Connections app is a good start.

[Return to Table of Contents](#Table-of-Contents)

___

## Features
* General Features
    * Login/Registration with validations
    * Single image lesson uses one image
    * Double image lesson connects two single image lessons to prompt deeper connections
* Teacher Features
    * Upload image to use as a prompt
    * Edit title, directions, and sentence starter for student prompt
    * Select whether students can "like" classmates' posts
    * Limit number of classmates' posts students can "like"
    * Select whether students need to provide a justification for "liking" a posts
    * Select whether posting and "liking" occur within same session or in separate sessions
    * View students' posts
    * Obtain link and code to lesson to share with students
* Student Features
    * Code screen for easy access to a lesson
    * Post a response to the lesson's prompt
    * View classmates' posts
    * If selected by teacher, "like" one or more classmates' posts
    * If selected by teacher, provide justification for their "like(s)"

[Return to Table of Contents](#Table-of-Contents)
___

## Technologies Used
* Python Django -- allows for future scalability
* HTML, CSS, and Bootstrap -- clean, responsive UI
* AJAX, jQuery, and RESTful routing -- render 24+ HTML templates while minimizing page reloads for smooth intuitive navigation and enhanced UX
* SQLite3 -- one-to-many and many-to-many relationships to connect users and lessons and allow for posts and "likes"
* HTML and Bootstrap validations as well as server-side validations and Bcrypt for secure login

[Return to Table of Contents](#Table-of-Contents)
___

## Screenshots -- Connections

![Landing Page](/Screenshots/1landing_page.png?raw=true)
![Login/Register](/Screenshots/2login_reg.png?raw=true)
![Student Dashboard](/Screenshots/3student_dashboard.png?raw=true)
![Single or Double Image Lesson](/Screenshots/4single_or_double.png?raw=true)
![Single Image Lesson Options](/Screenshots/5single_options.png?raw=true)
![Create New Single Image Lesson](/Screenshots/6new_single_lesson.png?raw=true)
![Single Image Lesson Preview](/Screenshots/7lesson_preview.png?raw=true)
![Successfully Created, Link Provided](/Screenshots/8success.png?raw=true)
![Code for Students](/Screenshots/9Code_for_students.png?raw=true)
![Justifications](/Screenshots/10justifications.png?raw=true)
!["Liking" classmates' posts](/Screenshots/11selecting_classmates_posts.png?raw=true)
![View Student Work](/Screenshots/12_view_student_work.png?raw=true)
![Double Image Lesson Options](/Screenshots/13double_options.png?raw=true)
![Edit Double Image Lesson](/Screenshots/14modify_double_lesson.png?raw=true)
![View Student Work Dougle Image Lesson](/Screenshots/15view_student_work_double.png?raw=true)

[Return to Table of Contents](#Table-of-Contents)

___

## Functionality
Upon logging in, the first screen to appear requests that students enter a code their teacher has given them to take them directly to the lesson page.  On the lesson page, students see the image and direction prompts provided by the teacher and are asked to post their observation(s).  Once they've posted, the posts of their classmates show up for them to peruse.  If the teacher has opted to allow students to "like" posts, the student is prompted to select posts that display good insights.  A light bulb next to selected posts turns on and the number of posts selected is tracked.  If the teacher opted to require a justification, a modal requesting the justification appears each time the student makes a selection.  Once the maximum number of "likes" set by the teacher has been reached, the student's page is routed to a thank you page. 

A link on the page where students can enter a code leads teachers to a page where they can choose whether they want to work with lessons that have a single image or two images.  Lesson options include creating a new lesson, modifying or deleting an existing lesson, looking at student work on a lesson, or obtaining a page with a lesson code that can be displayed at the front of a classroom for students.

Teachers can upload an image for a lesson and edit the title and directions for students.  Teachers also can select options like allowing students to "like" classmates' posts, requiring justifications for those "likes", limiting the number of "likes" allowed, and determining whether the "liking" of classmates' posts will occur within the same session or in a separate session from the initial posting.

Double image lessons combine two previously used single image lessons.  Students' posts from those single image lessons are listed on the double image lesson page for students to use as a reference when reflecting on the connection between the images and writing their posts.

[Return to Table of Contents](#Table-of-Contents)

___

## Design
I wanted to make this as user friendly as possible for students and teachers.  Students only need to log in and enter a code to reach the lesson for the day.  Teachers get a link and a code, either of which could be posted to online student materials or displayed on a screen at the front of the classroom.  I would love to add a Google Sign in to simplify the process even further and eliminate the forgotten password issue that can be such a hassle in the classroom.

Lesson options that a teacher might select are offered both during lesson creation and when navigating to the lesson code screen in case a teacher wants to make adjustments on the lesson day.  A lesson preview is offered during lesson creation so that the teacher can see what a student will see.  Some error prevention features were included in the design.  For example, if a single image lesson is deleted, related double image lessons are also deleted (after a warning message) in order to prevent errors.  The button for creating a double image lesson is deactivated until the teacher has selected two single image lessons.  

[Return to Table of Contents](#Table-of-Contents)

___

## Running Locally

These steps work on Windows and assume you have Python
1. Create virtual environment
    ```
    python -m venv name
    ```
    where name is whatever you want to call the environment 
2. Activate the virtual environment
    ```
    call name\Scripts\activate
    ```
    where name is the name of the virtual environment you created
3. Clone this repository
    ```
    git clone https://github.com/Purposefully/Connections.git
    ```
4. Move into the repository
    ```
    cd Connections
    ```
5. Install the dependencies
    ```
    pip install -r requirements.txt
    ```
6.  Move into the Connections app
    ```
    cd Connections
    ```
7.  Get a random secret key.  Using https://miniwebtool.com/django-secret-key-generator/ is one option.

8.  Create a secrets.py file and include a secret key
    ```
    notepad secrets.py
    ```
    Choose yes to create the file.
    Then type the following into the file.  Save and close.
    ```
    secret='paste secret key here'
    ```
9.  Move out of the app
    ``` 
    cd..
    ```
10. Migrate
    ```
    python manage.py migrate
    ```
11. Run a local server
    ```
    python manage.py runserver
    ```
12.  Open browser  
        ```
        localhost8000:
        ```

[Return to Table of Contents](#Table-of-Contents)
