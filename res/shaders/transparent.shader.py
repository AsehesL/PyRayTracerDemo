def lambertian_f(color, k):
	return k*color/math.pi

def lambertian_rho(color, k):
	return k*color

def tir(direction, normal, eta):
	wo = -1*direction
	cos_thetai = Vector3.dot(wo, normal)
	if cos_thetai < 0
		eta = 1.0 / eta
	return 1.0-(1.0-cos_thetai*cos_thetai)/(eta*eta)<0.0

def sample_f():
	pass

def glossy_specular_f(normal, lightDir, viewDir, color, k):
	L = Color.black
	refl = Vector3.reflect(normal, lightDir)
	ndr = Vector3.dot(refl, viewDir)
	if ndr > 0.0:
		return (ndr**k)*color

def main(hit, scene, output):
	acol = lambertian_rho(Color(am_color[0], am_color[1], am_color[2], am_color[3]), am_k)
	dcol = lambertian_f(Color(dif_color[0], dif_color[1], dif_color[2], dif_color[3]), dif_k)

	col = acol*scene.ambient.L(hit, scene)

	sepccol = Color(spec_color[0], spec_color[1], spec_color[2], spec_color[3])

	wo = -1*hit.ray.direction

	for light in scene.lights:
		ldir = light.get_direction(hit)
		inshadow = False
		if light.casts_shadows:
			sray = Ray(hit.point, ldir)
			inshadow = light.in_shadow(scene, sray)
		ndl = Vector3.dot(hit.normal.get_normalized(), ldir)
		if ndl <=0:
			continue
		if inshadow == False:
			col = col + (dcol+glossy_specular_f(hit.normal, ldir, wo, sepccol, glossy))* (ndl*light.G(hit)* light.L(hit, scene)/light.pdf(hit))

	cr = Color(cr_col[0],cr_col[1],cr_col[2],cr_col[3])

	vrefl = Vector3.reflect(wo, hit.normal)

	fr = kr*cr/Vector3.dot(vrefl, hit.normal)
	reflray = Ray(hit.point, vrefl)
	traceback = scene.tracer.trace(reflray, scene, 0.000001, hit.depth+1)
	if traceback:
		col = col + Vector3.dot(hit.normal, vrefl) * fr * traceback

	output['result'] = col