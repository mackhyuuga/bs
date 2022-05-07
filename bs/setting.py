import bpy

def select_particle(name, deselect_other = True, select = True, active = True):
    """ It select and activate objects

    Args:
        name (str): name of the object
        deselect_other (bool, optional): if it should deselect all the others objects. Defaults to True.
        select (bool, optional): Defaults to True.
        active (bool, optional): Defaults to True.
    """
    if deselect_other:
        bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[name].select_set(select)
    if active:
        bpy.context.view_layer.objects.active = bpy.data.objects[name]



def particle_visibility(name, hide_select = False, hide_in_viewport = False, globally_viewport = False, hide_render = False, particle_in_object_mode = True): 
    """It controls the visibility of the object 

    Args:
        name (str): the name of the object
        hide_select (bool, optional): disable the posibility of select the object . Defaults to False.
        hide_in_viewport (bool, optional): Defaults to False.
        globally_viewport (bool, optional): Defaults to False.
        hide_render (bool, optional): Defaults to False.
        particle_in_object_mode (bool, optional): at the end it puts on the object mode. Defaults to True.
    """
    select_particle(name) # calling the function select_particle

    bpy.data.objects[name].hide_select = hide_select
    bpy.context.active_object.hide_set(hide_in_viewport) 
    bpy.context.active_object.hide_viewport = globally_viewport
    bpy.data.objects[name].hide_render = hide_render

    if particle_in_object_mode and bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.editmode_toggle()



def object_mode(mode = 'OBJECT'):
    """ It change the object mode 

    Args:
        mode (str, optional): this variable can be 'OBJECT', 'EDIT' 'SCULPT', 'VERTEX_PAINT', 
        'WEIGHT_PAINT' or 'TEXTURE_PAINT'. Defaults to 'OBJECT'.
    """
    bpy.ops.object.mode_set(mode=mode)



def apply_transformations(name, location=True, rotation=True, scale=True):
    """
    This function reset informations about position, rotation and scale of the particle
    """
    particle_visibility(name)

    bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
    try:
        name.position = ((0,0,0) if location else name.position)
        name.rotation = ((0,0,0) if rotation else name.rotation)
        name.scale = ((0,0,0) if scale else name.sclae)
    except:
        pass



def creating_collection(collection_name):
    """ It creates a collection if it doesn't exist yet

    Args:
        collection_name (str)
    """
    exist = False
    for c in list(bpy.data.collections):
        if c.name == collection_name:
            exist = True
            break
    if exist is False:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)


def delete(name):
    """It delets particles

    Args:
        name (str): the name of the particle you want to delete
    """
    try:
        select_particle(name)
        bpy.ops.object.delete()
    except:
        pass


def putting_in_the_right_collection(object_name, collection_name):
    """ It link an object to a specific collection 

    Args:
        object_name (str)
        collection_name (str)
    """
    try:
        bpy.data.collections[collection_name].objects.link(bpy.data.objects[object_name])
        bpy.data.scenes['Scene'].collection.objects.unlink(bpy.data.objects[object_name])
    except:
        pass

    for c in list(bpy.data.collections):
        if c.name != collection_name:
            try:
                c.objects.unlink(bpy.data.objects[object_name])
            except:
                pass


def keyframe(name, frame, data_path = 'location'):
    """ It puts a keyframe

    Args:
        name (_type_): _description_
        frame (_type_): _description_
        data_path (str, optional): It can be "location", "rotation_euler", "scale", "hide_render". Defaults to 'location'.
    """
    bpy.data.objects[name].keyframe_insert(
    data_path = data_path,
    frame = frame
    )

def keyframe_vertices():
    bpy.data.window_managers['WinMan'].animall_properties['key_points']
    bpy.ops.anim.insert_keyframe_animall()



def delete_keyframe():
    pass