
def main(hit, scene, output):
	nor = hit.normal
	ndl = max(0, Vector3.dot(nor.getNormalized(), Vector3(0.2,-0.7,-0.6).getNormalized()))
	output['result'] = ndl*Color(1,1,1,1)