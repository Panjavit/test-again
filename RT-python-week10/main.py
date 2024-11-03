import RT_utility as rtu
import RT_camera as rtc
import RT_renderer as rtren
import RT_material as rtm
import RT_scene as rts
import RT_object as rto
import RT_integrator as rti
import RT_texture as rtt
import RT_light as rtl

def render_mickey_mouse_with_grass_and_sky():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0 / 9.0
    main_camera.img_width = 3840
    main_camera.samples_per_pixel = 10
    main_camera.max_depth = 5
    main_camera.vertical_fov = 80  # ขยายมุมกล้อง
    main_camera.look_from = rtu.Vec3(-3.0, 2.0, 2.0)  # ปรับตำแหน่งกล้องให้ถอยออก
    main_camera.look_at = rtu.Vec3(0, 0.4, -0.2)      # มองไปที่หัวมิกกี้
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    aperture = 1.0
    focus_distance = 5.0
    main_camera.init_camera(aperture, focus_distance)

    # Create a sky background
    bSkyBG = True

    # Define materials
    mat_black = rtm.Blinn(rtu.Color(0, 0, 0), 0.5, 0.5, 8)
    mat_skin = rtm.Blinn(rtu.Color(1.0, 0.8, 0.5), 0.5, 0.5, 8)
    mat_tree_trunk = rtm.Blinn(rtu.Color(0.55, 0.27, 0.07), 0.5, 0.5, 8)
    mat_leaves = rtm.Blinn(rtu.Color(0.1, 0.8, 0.1), 0.5, 0.5, 8)
    mat_road = rtm.Blinn(rtu.Color(0.5, 0.5, 0.5), 0.5, 0.5, 8)

    world = rts.Scene()

    # Add grass texture
    tex_grass = rtt.CheckerTexture(0.1, rtu.Color(0.2, 0.5, 0.2), rtu.Color(0.1, 0.3, 0.1))
    mat_grass = rtm.TextureColor(tex_grass)
    world.add_object(rto.Sphere(rtu.Vec3(0, -100.5, -1), 100, mat_grass))
    # ใบหน้า 
    world.add_object(rto.Sphere(rtu.Vec3(0.2, 0, -0.2), 0.5, mat_skin))
    # หูซ้าย
    world.add_object(rto.Sphere(rtu.Vec3(-0.2, 0.4, -0.1), 0.2, mat_black))
    # หูขวา
    world.add_object(rto.Sphere(rtu.Vec3(0.6, 0.4, -0.1), 0.2, mat_black))

    # เพิ่มต้นไม้
    for i in range(-2, 3):
        world.add_object(rto.Sphere(rtu.Vec3(i * 1.5, 0, -1), 0.15, mat_tree_trunk))
        world.add_object(rto.Sphere(rtu.Vec3(i * 1.5, 0.35, -1), 0.25, mat_leaves))

    # Add clouds with adjusted material properties
    cloud_material = rtm.Blinn(rtu.Color(1.0, 1.0, 1.0), 1.0, 1.0, 10)
    cloud_positions = [
        rtu.Vec3(2, 2, 2),
        rtu.Vec3(2.5, 2, 2),
        rtu.Vec3(2.5, 2.2, 2),
        rtu.Vec3(3, 2, 2),
        rtu.Vec3(1, 2.5, -4),
        rtu.Vec3(1.5, 2.8, -4),
        rtu.Vec3(1.5, 2.5, -4),
        rtu.Vec3(2, 2.5, -4),
        rtu.Vec3(2.5, 2, -2),
        rtu.Vec3(3, 2, -2),
        rtu.Vec3(3, 2.2, -2),
        rtu.Vec3(3.5, 2, -2),
    ]

    for pos in cloud_positions:
        world.add_object(rto.Sphere(pos, 0.3, cloud_material))

    # Add a road
    road_width = 2.0  # ทำให้ถนนกว้างขึ้น
    road_length = 30.0  # เพิ่มความยาวของถนน
    road_height = -0.5  # ปรับตำแหน่งถนนให้สูงขึ้น
    road_pos = rtu.Vec3(-road_length / 2, road_height, -1)  # จัดตำแหน่งให้ถนนอยู่ตรงกลางฉาก
    u_vector = rtu.Vec3(road_length, 0, 0)
    v_vector = rtu.Vec3(0, 0, road_width)
    world.add_object(rto.Quad(road_pos, u_vector, v_vector, mat_road))



    # เพิ่มตึก
    building_height = 1.5
    building_width = 1.0
    building_depth = 1.0
    building_material = rtm.Blinn(rtu.Color(1.0, 0.9, 0.8), 0.5, 0.5, 8)  # สีครีม

    # สร้าง 3 ตึก
    for j in range(3):
        building_pos = rtu.Vec3(1.5 + j * 1.5, 0, -2)  # ปรับตำแหน่งตึก
        # สร้างกำแพงตึก
        world.add_object(rto.Quad(building_pos, rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, building_height, 0), building_material))  # ด้านหน้า
        world.add_object(rto.Quad(building_pos + rtu.Vec3(0, 0, -building_depth), rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, building_height, 0), building_material))  # ด้านหลัง
        world.add_object(rto.Quad(building_pos, rtu.Vec3(0, 0, -building_depth), rtu.Vec3(0, building_height, 0), building_material))  # ด้านข้างซ้าย
        world.add_object(rto.Quad(building_pos + rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, 0, -building_depth), rtu.Vec3(0, building_height, 0), building_material))  # ด้านข้างขว

    # เพิ่มตึกสูงขึ้นทางซ้าย
    tall_building_height = 2.5  # สูงกว่าตึกเดิม
    tall_building_pos = rtu.Vec3(-1.5, 0, -2)  # ปรับตำแหน่งให้ไปทางซ้าย

    # สร้างกำแพงตึกสูง
    world.add_object(rto.Quad(tall_building_pos, rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, tall_building_height, 0), building_material))  # ด้านหน้า
    world.add_object(rto.Quad(tall_building_pos + rtu.Vec3(0, 0, -building_depth), rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, tall_building_height, 0), building_material))  # ด้านหลัง
    world.add_object(rto.Quad(tall_building_pos, rtu.Vec3(0, 0, -building_depth), rtu.Vec3(0, tall_building_height, 0), building_material))  # ด้านข้างซ้าย
    world.add_object(rto.Quad(tall_building_pos + rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, 0, -building_depth), rtu.Vec3(0, tall_building_height, 0), building_material))  # ด้านข้างขวา

    # เพิ่มตึกเตี้ยทางซ้ายของตึกสูง
    short_building_height = 1.0  # ความสูงตึกเตี้ย
    short_building_pos = rtu.Vec3(-2.5, 0, -2)  # ปรับตำแหน่งให้ไปทางซ้าย

    # สร้างกำแพงตึกเตี้ย
    world.add_object(rto.Quad(short_building_pos, rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, short_building_height, 0), building_material))  # ด้านหน้า
    world.add_object(rto.Quad(short_building_pos + rtu.Vec3(0, 0, -building_depth), rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, short_building_height, 0), building_material))  # ด้านหลัง
    world.add_object(rto.Quad(short_building_pos, rtu.Vec3(0, 0, -building_depth), rtu.Vec3(0, short_building_height, 0), building_material))  # ด้านข้างซ้าย
    world.add_object(rto.Quad(short_building_pos + rtu.Vec3(building_width, 0, 0), rtu.Vec3(0, 0, -building_depth), rtu.Vec3(0, short_building_height, 0), building_material))  # ด้านข้างขวา


    # กำหนดตำแหน่ง สี และความเข้มของแสง
    light_position = rtu.Vec3(5, 5, -5)
    light_color = rtu.Color(1.0, 1.0, 1.0)
    light_intensity = 1.0

    # เพิ่มแสงเข้าไปในฉากโดยใช้ Diffuse_light
    diffuse_light = rtl.Diffuse_light(light_color * light_intensity)

    # เพิ่มแสงเข้าไปในฉาก
    world.add_object(rto.Sphere(light_position, 0.1, diffuse_light))

    # Render
    intg = rti.Integrator(bSkyBG=bSkyBG)
    renderer = rtren.Renderer(main_camera, intg, world)
    renderer.render()
    renderer.write_img2png('mickey_mouse_grass_sky_with_buildings.png')

if __name__ == "__main__":
    render_mickey_mouse_with_grass_and_sky()
