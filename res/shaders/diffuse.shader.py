def main(hit, scene, reflcol, output):
	acol = Color(am_color[0], am_color[1], am_color[2], am_color[3])
	amk = am_k
	dcol = Color(dif_color[0], dif_color[1], dif_color[2], dif_color[3])
	difk = dif_k

	#amcl = Color.black
	#for i in range(0, 16):
	#	amcl += scene.ambient.L(hit, scene)
	#amcl = amcl/16
	#col = amk*acol*amcl
	col = amk*acol*scene.ambient.L(hit, scene)
	#col = amk*acol*scene.ambient_occluder.L(hit, scene)


	for light in scene.lights:
		ldir = light.get_direction(hit)
		inshadow = False
		if light.casts_shadows:
			sray = Ray(hit.point, ldir)
			inshadow = light.in_shadow(scene, sray)
		ndl = max(0, Vector3.dot(hit.normal.get_normalized(), ldir))
		if inshadow == False:
			col = col + (difk*dcol/3.1415926)* (ndl*light.G(hit)* light.L(hit, scene)/light.pdf(hit))

	output['result'] = col

