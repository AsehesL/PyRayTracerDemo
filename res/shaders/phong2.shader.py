def main(hit, scene, output):
	acol = Color(am_color[0], am_color[1], am_color[2], am_color[3])
	amk = am_k
	dcol = Color(dif_color[0], dif_color[1], dif_color[2], dif_color[3])
	difk = dif_k

	col = amk*acol*scene.ambient.L(hit, scene)

	sepccol = Color(spec_color[0], spec_color[1], spec_color[2], spec_color[3])

	wo = -1*hit.ray.direction

	for light in scene.lights:
		ldir = light.get_direction(hit)
		inshadow = False
		if light.casts_shadows:
			sray = Ray(hit.point, ldir)
			inshadow = light.in_shadow(scene, sray)
		ndl = Vector3.dot(hit.normal.get_normalized(), ldir)
		refl = Vector3.reflect(ldir, hit.normal)
		rdwo = Vector3.dot(refl, wo)
		if ndl <=0:
			continue
		if inshadow == False:
			c = difk*dcol/3.1415926
			if rdwo > 0.0:
				c += (rdwo**glossy)*sepccol
			col = col + c* (ndl*light.G(hit)* light.L(hit, scene)/light.pdf(hit))

	#cr = Color(cr_col[0],cr_col[1],cr_col[2],cr_col[3])

	#vrefl = Vector3.reflect(wo, hit.normal)

	#fr = kr*cr/Vector3.dot(vrefl, hit.normal)
	#reflray = Ray(hit.point, vrefl)
	#traceback = scene.tracer.trace(reflray, scene, 0.000001, hit.depth+1)
	#if traceback:
	#	col = col + Vector3.dot(hit.normal, vrefl) * fr * traceback

	output['result'] = col