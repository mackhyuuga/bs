# import bpy
import math
import numpy as np
import pandas as pd


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Scene():

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
            obj.hide_set(False)
            obj.hide_select = False
            obj.hide_viewport = False

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




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def setting_particle(self, creating):
    """
    This function contains the functions responsible to delete previous objects with the same name as the one that is being created,
    as well as creating a collection and putting the object in the right collection
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
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[self.name].select_set(True)
                bpy.context.view_layer.objects.active =  bpy.data.objects[self.name]
                bpy.data.objects[self.name].hide_render = False
                if bpy.context.active_object.mode == 'EDIT':
                    bpy.ops.object.editmode_toggle()
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
# Executting the internal functions
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    creating_collection()
    if self.delete_previous:
        deleting_previous()
    creating()
    putting_in_the_right_collection()





#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Particle():
    """This class create a particle with the following characteristics:
       Parameters
       ----------
       name : string
       position : array (x,y,z)
       rotation : array (x,y,z)
       scale : array (x,y,z)
       collection : string : (It is the name of the collection to which the particle belongs),
       data (For when we want to link this particle with a database contanins informations such as the path, the momento, charge, and so on)
     """
     
    def __init__(self, name = 'particle', collection = 'Collection', position = None, rotation = None, scale = None, data = None):
        self.name = name
        self.collection = collection
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.data = data



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Functions responsible to oprations of moving, rotating and resizing
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def move(self, location = (0,0,0)):
            bpy.data.objects[self.name].location = location


    def rotate(self, rotation_euler = (0,0,0)):
            bpy.data.objects[self.name].rotation_euler = rotation_euler


    def size(self, scale = (1,1,1)):
            bpy.data.objects[self.name].scale = scale


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Getting and setting the vertices
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    @property
    def vertex(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self.name].select_set(True)
        bpy.context.view_layer.objects.active =  bpy.data.objects[self.name]
        v = []
        for vert in bpy.context.active_object.data.vertices:
            v.append(vert.co)
        return v

    def set_vertices(self, vertex, coordinate):
            bpy.data.objects[self.name].select_set(True)
            bpy.context.active_object.data.vertices[vertex].co = coordinate


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


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Sphere(Particle):
    def __init__(self, name = 'sphere', collection = 'Collection', position = (0, 0, 0), rotation = (0, 0, 0), scale = (1,1,1), data = None, delete_previous = True):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data)
        self.delete_previous = delete_previous

        setting_particle(self, self.creating)


    def creating(self):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=self.position, scale=self.scale)
        bpy.context.object.name = self.name




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Camera(Particle):
    def __init__(self, name='camera', collection = 'Collection', position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1), focal_length = 85, data = None, delete_previous = True):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data)
        self.focal_length = focal_length
        self.delete_previous = delete_previous

        setting_particle(self, self.creating)


    def creating(self):
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=self.position, rotation=self.rotation, scale=self.scale)
        bpy.context.object.name = self.name
        bpy.context.object.data.lens = self.focal_length








#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Timer(Particle):
    def __init__(self, name = 'timer', collection = 'Collection', position = (0,0,0), rotation = (0,0,0), scale = (1,1,1), frame = 24, data = None, delete_previous = True):
        super().__init__(name = name, collection = collection, position = position, rotation = rotation, scale = scale, data = data)
        self.frame = frame
        self.delete_previous = delete_previous

        setting_particle(self, self.creating)


    def creating(self):
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



#class Text(Particle):
#    def __init__(self, name, position = (0, 0, 0)):
#        super().__init__(name = name, position = position)
#
#
#    def create(self, context, location = (0, 0, 0)):
#        if delete_previous:
#            self.delete_previous()
#
#        bpy.ops.object.text_add(enter_editmode=True, location=location)
#        bpy.context.object.name = self.name
#        bpy.ops.font.delete(type='PREVIOUS_WORD')
#        bpy.ops.font.text_insert(text= context)
#
#
#    def rewrite(self, context, location = (0,0,0)):
#        bpy.data.objects[self.name].select_set(True)
#        bpy.ops.object.editmode_toggle()
#        bpy.ops.font.delete(type='PREVIOUS_WORD')
#        bpy.ops.font.text_insert(text= contxt)
#        bpy.ops.object.editmode_toggle()


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == "__main__":


#    Scene.clean_scene()


#    df = pd.read_csv('/home/allison/Documents/facul/computacional/código/output_01.txt', delimiter = '\s+')


#    scale = np.array((0.1,0.1,0.1))




#    particle1 = Sphere('particle1', position = (0,0,0), scale=4*scale)
#    particle2 = Sphere('particle2', position = (0,0,0), scale=1*scale)
#    particle3 = Sphere('particle3', position = (0,0,0), scale=1*scale)

#    particle1.path = df[['r1x', 'r1y']]
#    particle2.path = df[['r2x', 'r2y']]
#    particle3.path = df[['r3x', 'r3y']]
#    print(particle1.path)




#    for i in range(1, df['t'].size):
#        particle1.move((particle1.path.r1x[i], particle1.path.r1y[i], 0))
#        particle2.move((particle2.path.r2x[i], particle2.path.r2y[i], 0))
#        particle3.move((particle3.path.r3x[i], particle3.path.r3y[i], 0))


#        particle1.keyframe(i)
#        particle2.keyframe(i)
#        particle3.keyframe(i)


#    s1 = Sphere("allison")
#    c1 = Camera()
    t1 = Timer()
