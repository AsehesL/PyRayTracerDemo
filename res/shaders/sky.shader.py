def main(hit, scene, output):
	sundir = Vector3(sun_dir[0], sun_dir[1], sun_dir[2]).get_normalized()
	col = Color.black

	sign = 0 if 0 > hit.ray.direction.y else 1

	hort = abs(hit.ray.direction.y)
	if hort < 0:
		hort = 0
	elif hort > 1.0:
		hort = 1.0
	hort = 1 - hort

	skyC = Color.lerp(Color(0.302, 0.38, 0.537), Color(0.435, 0.545, 0.702), 2**(hort*1.4-1.4))
	groundC = Color.lerp(Color(0.412, 0.384, 0.365), Color(0.435, 0.545, 0.702), 2**(hort * 4.4 * 2.7 - 4.4 * 2.7))

	col += Color.lerp(groundC, skyC, sign)

	col += 0.3 * (2 **(hort * 20.0 - 20.0)) * Color(0.8, 0.9, 1.0)
	col += 0.1 * (2 **(hort * 15.0 - 15.0)) * Color(0.8, 0.9, 1.0)

	sun = Vector3.dot(sundir, hit.ray.direction)
	if sun < 0:
		sun = 0
	elif sun > 1.0:
		sun = 1.0
	col += 0.2 * (sun**2.0) * Color(1.0, 0.8, 0.2)
	col += 0.5 * (2**(sun*650-650)) * Color(1.0, 0.8, 0.9)
	col += 0.1 * (2**(sun*100-100)) * Color(1.0, 1.0, 0.8)
	col += 0.3 * (2**(sun*50-50)) * Color(1.0, 0.8, 0.8)
	col += 0.5 * (2**(sun*10-10)) * Color(0.7, 0.3, 0.05)

	col.a = 0

	output['result'] = col