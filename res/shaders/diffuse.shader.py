def main(hit, scene, reflcol, output):
	acol = Color(am_color[0], am_color[1], am_color[2], am_color[3])
	amk = am_k
	dcol = Color(dif_color[0], dif_color[1], dif_color[2], dif_color[3])
	difk = dif_k

	col = amk*acol*scene.ambient.L(hit)



	for light in scene.lights:
		ldir = light.get_direction(hit)
		inshadow = False
		if light.casts_shadows:
			sray = Ray(hit.point, ldir)
			inshadow = light.in_shadow(scene, sray)
		ndl = max(0, Vector3.dot(hit.normal.get_normalized(), ldir))
		if inshadow == False:
			col = col + (difk*dcol/3.1415926)* (ndl* light.L(hit))

	output['result'] = col
