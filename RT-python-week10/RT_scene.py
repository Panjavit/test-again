# Scene class
import RT_utility as rtu
import numpy as np
import RT_object as rto

class Scene:
    def __init__(self):
        self.objects = []  # ใช้ objects แทน obj_list
        self.lights = []  # เพิ่มรายการแสง
        self.light_list = []  # กำหนดแอตทริบิวต์ light_list
        self.point_light_list = []  # กำหนดแอตทริบิวต์ point_light_list
        self.background_color = rtu.Color(0, 0, 0)  # กำหนดสีพื้นหลังถ้ายังไม่ได้ตั้งไว้

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):  # เพิ่มเมธอด add_light
        self.lights.append(light)

    def find_intersection(self, vRay, cInterval):
        np_obj_list = np.array(self.objects)  # เปลี่ยนเป็น self.objects
        found_hit = False
        closest_tmax = cInterval.max_val
        hinfo = None
        for obj in np_obj_list:
            hinfo = obj.intersect(vRay, rtu.Interval(cInterval.min_val, closest_tmax))
            if hinfo is not None:
                closest_tmax = hinfo.getT()
                found_hit = True
                self.hit_list = hinfo
        return found_hit

    def find_occlusion(self, vRay, cInterval):
        np_obj_list = np.array(self.objects)  # เปลี่ยนเป็น self.objects
        closest_tmax = cInterval.max_val
        number_of_hit = 0
        for obj in np_obj_list:
            hinfo = obj.intersect(vRay, rtu.Interval(cInterval.min_val, closest_tmax))
            if hinfo is not None:
                number_of_hit += 1

        return number_of_hit > 1  # คืนค่าถ้ามีการชนมากกว่า 1

    def getHitNormalAt(self, idx):
        return self.hit_list[idx].getNormal() 

    def getHitList(self):
        return self.hit_list

    def getBackgroundColor(self):
        return self.background_color

    def get_sky_background_color(self, rGen_ray):
        unit_direction = rtu.Vec3.unit_vector(rGen_ray.getDirection())
        a = (unit_direction.y() + 1.0) * 0.5
        # ปรับสีให้เข้มขึ้น
        bright_color = rtu.Color(1.0, 1.0, 1.0) * (1.0 - a)  # สีขาว
        blue_color = rtu.Color(0.3, 0.6, 0.9) * a  # สีฟ้าครามเข้มขึ้น
        return bright_color + blue_color
    
    def find_lights(self):
        np_obj_list = np.array(self.lights)  # เปลี่ยนเป็น self.lights
        for obj in np_obj_list:
            if obj.material.is_light():
                self.light_list.append(obj)

        self.find_point_lights()

    def find_point_lights(self):
        for light in self.light_list:
            if isinstance(light, rto.Sphere):
                self.point_light_list.append(light)
