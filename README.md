# lms


### Course
    Each course will be divided into a
    configurable number of modules, and each module will contain a configurable number of contents.
    The contents will be of various types: text, files, images, or videos
    Subject 1 => Course 1 => Module 1
    These are the initial Subject , Course , and Module models. The Course model fields are as follows:
    • owner : The instructor who created this course.
    • subject : The subject that this course belongs to. It is a ForeignKey field that points to the
    Subject model.
    • title : The title of the course.
    • slug : The slug of the course. This will be used in URLs later.
    • overview : A TextField column to store an overview of the course.
    • created : The date and time when the course was created