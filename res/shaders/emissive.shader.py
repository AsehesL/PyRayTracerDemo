def main(hit, scene, output):
	#ndr = max(0, Vector3.dot(-1*hit.normal, hit.ray.direction))
	col = Color(ce[0], ce[1], ce[2], ce[3])
	output['result'] = ls*col

def em_main(hit, scene, output):
	col = Color(ce[0], ce[1], ce[2], ce[3])

	output['result'] = ls*col

