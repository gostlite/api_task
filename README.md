# api_task
Api to perform crud functions

Here are the instructions on how to use the site sir.

You can just login using the test login   /login which takes keys of email and password. Email: test@mail.com, password: pass.

Alternatively you can register

1. Register : /register, this takes only post request of keys: {first_name, last_name, email, password}

2. Login: /login which takes keys of email and password.

3. List all templates: /template, This can only be achieved by login in.

4. Add new template: /newtemplate , this takes keys of template_name, subject and body. Only logged in users can do this.

5. Delete template: /delete/<template_id> this accepts only DELETE method and only logged in user can delete thier post, you can't delete others post

6. Edit post: /template/<template_id>, this takes the PUT method, only logged in user can edit thier post, you can't edit others post.
