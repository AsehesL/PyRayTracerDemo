
def main(hit, scene, output):
	nor = hit.normal
	ndl = max(0, Vector3.dot(nor.get_normalized(), Vector3(0.321,0.766,-0.557).get_normalized()))

	col = Color(color[0],color[1],color[2],color[3])

	#if reflcol != None:
	#	col = Color.lerp(col, reflcol, 0.5)

	output['result'] = ndl*col