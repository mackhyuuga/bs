import bpy
import math
import numpy as np
import pandas as pd

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Scene settings 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Scene():
    """This class contains functions to configure the scene 
    """
    @staticmethod
    def frame_format(format = [1920, 1800]):
        """
        This function defines the format of the scene frame,
        by default the format is 1920 by 1800
        """
        bpy.context.scene.render.resolution_x = format[0]
        bpy.context.scene.render.resolution_y = format[1]

    @staticmethod
    def purge_orphans():
        if bpy.app.version >= (3, 0, 0):
            bpy.ops.outliner.orphans_purge(
                do_local_ids=True, do_linked_ids=True, do_recursive=True
            )
        else:
            # call purge_orphans() recursively until there are no more orphan data blocks to purge
            result = bpy.ops.outliner.orphans_purge()
            if result.pop() != "CANCELLED":
                purge_orphans()


    @classmethod
    def clean_scene(cls):
        """
        Removing all of the objects, collection, materials, particles,
        textures, images, curves, meshes, actions, nodes, and worlds from the scene
        """
        if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
            bpy.ops.object.editmode_toggle()

        for obj in bpy.data.objects:
            obj.hide_render_set(False)
            obj.hide_render_select = False
            obj.hide_render_viewport = False

        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

        collection_names = [col.name for col in bpy.data.collections]
        for name in collection_names:
            bpy.data.collections.remove(bpy.data.collections[name])

        # in the case when you modify the world shader
        world_names = [world.name for world in bpy.data.worlds]
        for name in world_names:
            bpy.data.worlds.remove(bpy.data.worlds[name])
        # create a new world data block
        bpy.ops.world.new()
        bpy.context.scene.world = bpy.data.worlds["World"]

        cls.purge_orphans()

    @classmethod
    def set_timeline(timeline):
        """
        It puts the time line at some position
        """
        bpy.context.scene.frame_set(timeline)


    @staticmethod
    def transformation_pivot_point(type):
        """This function change the transformation pivot point

        Args:
            type (str): bounding box center, cursor, individual origins, median point, active element
        """
        if type == "bounding box center":
            bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

        elif type == "cursor":
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        elif type == "individual origins":
            bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'

        elif type == "median point":
            bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

        elif type == "active element":
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'


    @staticmethod
    def transformation_orientation(type):
        """This function change the transformation orientation

        Args:
            type (str): global, local, normal, gimbal, view, cursor
        """
        if type == "global":
            bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'

        elif type == "local":
            bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'

        elif type == "normal":
            bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'

        elif type == "gimbal":
            bpy.context.scene.transform_orientation_slots[0].type = 'GIMBAL'

        elif type == "view":
            bpy.context.scene.transform_orientation_slots[0].type = 'VIEW'

        elif type == "cursor":
            bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Exterior functions for the Particle class
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def particle_visibility(self, deselect_other = True, hide_viewport = False, hide_render = False, globally_viewport = False): 
    """This function is responsable to activate objects of the scene

    Args:
        deselect_other (bool, optional): Defaults to True.
        hide_render (bool, optional): it is responsable for hide_render the object. Defaults to False.
    """
    if deselect_other:
        bpy.ops.object.select_all(action='DESELECT')
    
    bpy.data.objects[self.name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[self.name]
    bpy.context.active_object.hide_set(hide_viewport) 
    bpy.data.objects[self.name].hide_render = hide_render
    bpy.context.active_object.hide_viewport = globally_viewport
    if bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def setting_particle(self, setting):
    """This function contains the functions responsible to delete previous objects with the name as the one that is being created,
    as well as create a collection and putting the object in the right collection
    Args:
        setting (list): It is a list with four booleans that define with the function:

            creating_collection
            deleting_previous
            create_particle_shape
            putting_in_the_right_collection

        will be executed.
    """
    
    def creating_collection():
            exist = False
            for i in range(0, len(bpy.data.collections)):
                if bpy.data.collections[i].name == self.collection:
                    exist = True
                    break
            if exist == False:
                collection = bpy.data.collections.new(self.collection)
                bpy.context.scene.collection.children.link(collection)


    def deleting_previous():
            try:
                particle_visibility(self)
                bpy.ops.object.delete()
            except:
                pass


    def putting_in_the_right_collection():
        try:
            bpy.data.collections[self.collection].objects.link(bpy.data.objects[self.name])
            bpy.data.scenes['Scene'].collection.objects.unlink(bpy.data.objects[self.name])
        except:
            pass

        for i in range(0, len(bpy.data.collections)):
            if bpy.data.collections[i].name != self.collection:
                try:
                    bpy.data.collections[i].objects.unlink(bpy.data.objects[self.name])
                except:
                    pass

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Executting the internal functions of setting particle function 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    if setting[0]:
        creating_collection()
    if setting[1]:
        deleting_previous()
    if setting[2]:
        self.create_particle_shape()
    if setting[3]:
        putting_in_the_right_collection()



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Particle classes
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Particle():
    """This class create a particle with the following characteristics:
       Parameters
       ----------
       name : string
       position : array (x,y,z)
       rotation : array (yz,zx,xy)
       scale : array (sx,sy,sz)
       collection : string : (It is the name of the collection to which the particle belongs),
       data (For when we want to link this particle with a database contanins informations such as the path, the momento, charge, and so on)
     """

    def __init__(self, name = 'particle', collection = 'Collection', position = None, rotation = None, scale = None, setting = (True, False, False, True), data = None):
        self.name = name
        self.collection = collection
        self.position = (position if position != None else (bpy.data.objects[self.name].location[0], bpy.data.objects[self.name].location[1], bpy.data.objects[self.name].location[2]))
        self.rotation = (rotation if rotation != None else (bpy.data.objects[self.name].rotation_euler[0], bpy.data.objects[self.name].rotation_euler[1], bpy.data.objects[self.name].rotation_euler[2]))
        self.scale = (scale if scale != None else (bpy.data.objects[self.name].scale[0], bpy.data.objects[self.name].scale[1], bpy.data.objects[self.name].scale[2]))
        self.setting = setting
        self.data = data

        
        setting_particle(self, self.setting)



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Functions responsible to oprations of moving, rotating and resizing
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def move(self, x = 0, y = 0, z = 0):
        bpy.data.objects[self.name].location = (x, y, z)
        self.position = (x, y, z)


    def rotate(self, yz = 0, zx = 0, xy = 0):
        bpy.data.objects[self.name].rotation_euler = (yz, zx, xy)
        self.rotation = (yz, zx, xy)


    def resize(self, sx = 1, sy = 1, sz = 1):
        bpy.data.objects[self.name].scale = (sx, sy, sz)
        self.scale = (sx, sy, sz)


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Getting and setting the vertices
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    @property
    def vertices(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self.name].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[self.name]
        return [v.co for v in bpy.context.active_object.data.vertices] 

    def set_vertices(self, vertex, new_coordinate):
        if bpy.context.active_object.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self.name].select_set(True)
        bpy.context.active_object.data.vertices[vertex].co = new_coordinate


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def apply_transformations(self, location=True, rotation=True, scale=True):
        """
        This function reset informations about position, rotation and scale of the particle
        """
        particle_visibility(self)

        bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
        self.position = ((0,0,0) if location else self.position)
        self.rotation = ((0,0,0) if rotation else self.rotation)
        self.scale = ((0,0,0) if scale else self.sclae)



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Putting a keyframe
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def keyframe(self, frame, data_path = 'location'):
        """
        It puts a keyframe
        """
        bpy.data.objects[self.name].keyframe_insert(
        data_path = data_path,
        frame = frame
    )


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Modifiers
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def create_modifier(self, name_of_modifier = "My_Modifier", type_of_modifier = "SUBSURF"):
        particle_visibility(self)
        bpy.context.active_object.modifiers.new(name_of_modifier, type_of_modifier)

    def skin(self, name_of_modifier = "Skin"):
        bpy.context.active_object.modifiers.new(name_of_modifier,"SKIN")
    
    def shade_smooth(self):
        particle_visibility(self)
        bpy.ops.object.shade_smooth()   
     




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Creating paticles with a specific format
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Sphere(Particle):
    def __init__(self, name = 'sphere', collection = 'Collection', position = (0, 0, 0), rotation = (0, 0, 0), scale = (1,1,1), data = None, setting = (True, True, True, True)):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data, setting = setting)

    def create_particle_shape(self):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=self.position, scale=self.scale)
        bpy.context.object.name = self.name




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Mesh(Particle):
    def __init__(self, name = 'mesh', collection = 'Collection', position = (0, 0, 0), rotation = (0, 0, 0), scale = (1,1,1), verts = [], edges = [], faces = [], data = None, setting = (True, True, True, True)):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data, setting = setting)
        self.verts = verts 
        self.edges = edges 
        self.faces = faces


    def create_particle_shape(self):
        # verts = bpy.context.active_object.data.vertices
        # edges = bpy.context.active_object.data.edges
        # faces = bpy.context.active_object.data.polygons

        mesh = bpy.data.meshes.new(self.name)
        obj = bpy.data.objects.new(self.name, mesh)
        col = bpy.data.collections.get(self.collection)
        col.objects.link(obj)
        bpy.context.view_layer.objects.active = obj 
        mesh.from_pydata(self.verts, self.edges, self.faces)




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Camera(Particle):
    def __init__(self, name='camera', collection = 'Collection', position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1), focal_length = 85, data = None, setting = (True, True, True, True)):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data, setting = setting)
        self.focal_length = focal_length


    def create_particle_shape(self):
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=self.position, rotation=self.rotation, scale=self.scale)
        bpy.context.object.name = self.name
        bpy.context.object.data.lens = self.focal_length



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Timer(Particle):
    def __init__(self, name = 'timer', collection = 'Collection', position = (0,0,0), rotation = (0,0,0), scale = (1,1,1), frame = 24, data = None, setting = (True, True, True, True)):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data, setting = setting)
        self.frame = frame


    def create_particle_shape(self):
        bpy.ops.object.text_add(enter_editmode=False,  align='WORLD', location=self.position, rotation=self.rotation, scale=self.scale)
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = 0.02
        bpy.context.object.data.align_x = 'CENTER'
        bpy.context.object.data.align_y = 'CENTER'
        bpy.context.object.name = self.name

        scene = bpy.context.scene
        obj = scene.objects[self.name]


        def recalculate_text(scene):


            if scene.frame_current in range(0, 60*self.frame):
                obj.data.body = str(int(bpy.context.scene.frame_current/self.frame)) + 's'

            else:
                min = int(bpy.context.scene.frame_current/self.frame) // 60
                obj.data.body = str(min) + 'min  ' + str(int(bpy.context.scene.frame_current/self.frame)-60*min) + 's'

        bpy.app.handlers.frame_change_post.append(recalculate_text)




if __name__ == "__main__":
    m = Mesh(verts = ((0,1,0),(1,0,0),(0,0,1),(-1,0,0)), edges = ([0,1],[1,2],[0,2],[0,3],[2,3]), faces = ([0,1,2],[2,0,3]))
    

# import bpy


# verts = ((0,1,0),(1,0,0),(0,0,1),(-1,0,0))
# edges = ([0,1],[1,2],[0,2],[0,3],[2,3])
# faces = ([0,1,2],[2,0,3])

# name = "New Object"
# mesh = bpy.data.meshes.new(name)
# obj = bpy.data.objects.new(name, mesh)
# col = bpy.data.collections.get("Collection")
# col.objects.link(obj)
# bpy.context.view_layer.objects.active = obj
# mesh.from_pydata(verts,edges,faces)