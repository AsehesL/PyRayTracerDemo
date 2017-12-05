def lambertian_f(color, k):
	return k*color/math.pi

def lambertian_rho(color, k):
	return k*color

def main(hit, scene, output):
	acol = lambertian_rho(Color(am_color[0], am_color[1], am_color[2], am_color[3]), am_k)
	dcol = lambertian_f(Color(dif_color[0], dif_color[1], dif_color[2], dif_color[3]), dif_k)

	col = acol*scene.ambient.L(hit, scene)

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
			col = col + dcol* (ndl*light.G(hit)* light.L(hit, scene)/light.pdf(hit))

	output['result'] = col

