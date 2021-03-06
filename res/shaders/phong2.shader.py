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

	cr = Color(cr_col[0],cr_col[1],cr_col[2],cr_col[3])

	vrefl = Vector3.reflect(wo, hit.normal)

	w = vrefl.get_normalized()
	u = Vector3.cross(Vector3(0.00424,1,0.00764), w)
	u.normalize()
	v = Vector3.cross(u, w)

	sp = sampler.sample_hemisphere()
	wi = sp.x*u+sp.y*v+sp.z*w

	if Vector3.dot(wi, hit.normal) < 0.0:
		wi = -sp.x*u-sp.y*v-sp.z*w

	phong_lobe = (Vector3.dot(vrefl, wi))**exp
	pdf = phong_lobe*Vector3.dot(hit.normal, wi)

	fr = phong_lobe*kr*cr

	reflray = Ray(hit.point, wi)
	traceback = scene.tracer.trace(reflray, scene, 0.000001, hit.depth+1)
	if traceback:
		col = col + Vector3.dot(hit.normal, wi) * fr/pdf * traceback

	output['result'] = col