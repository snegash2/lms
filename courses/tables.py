from django_tables2 import Column, tables
from .models import Course
from django.utils.safestring import mark_safe


class CourseTable(tables.Table):
    # actions = Column()
 
    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ('published','course_type', 'has_practice','created','students','id')
        # exclude = ("teacher",'image','slug','reason_not_published')
        
        
    id = Column(verbose_name='actions')
#
    def render_id(self, value):
        # perform custom logic and data retrieval (if needed)

        # generate button HTML based on data and desired behavior
        
        button_html = f'''
        
        
                
        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Delete with id {value} </h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                Are you sure you want to delete this {value}?
                </div>
                <div class="modal-footer">
                <button type="button" id="modal-delete-btn" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-danger" onclick = "deleteId({value})">Delete</button>
                </div>
            </div>
            </div>
            </div>
         <div>
    
        <a href="/course/{value}/edit/">
          <button  class="btn btn-small" type="button">View Course</button>
        </a>
           
           
        <a href="#">
          <button  class="btn btn-small" >Students</button>
        </a>

    
        <a href="#">
          <button class="btn small">Add Module</button>
        </a>
        <a>
          <button class="btn btn-samll" style="background-color: brown;" id="delete-btn" onclick="deleteAction({value})" data-bs-toggle="modal"  data-bs-target="#exampleModal">Delete</button>

        </a>

    </div>
        '''

        return mark_safe(button_html)
        
 
   
 