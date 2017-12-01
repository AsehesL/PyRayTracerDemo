def main(hit, scene, reflcol, output):
	ndr = max(0, Vector3.dot(-1*hit.normal, hit.ray.direction))
	col = Color(ce[0], ce[1], ce[2], ce[3])
	output['result'] = ndr*ls*col

def em_main(hit, scene, reflcol, output):
	col = Color(ce[0], ce[1], ce[2], ce[3])

	output['result'] = col

