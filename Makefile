prepRAs:
	echo "choose prepRA step"
	python reorderFunctWASMooney.py

checkRA:
	echo “checkRA step”
	python reorderFunctWASMooney.py

correctPerm:
	echo “correct from permissive step”
	python reorderFunctWASMooney.py

pullOtherVars:
	echo “pull other vars step”
	python reorderFunctWASMooney.py

mergeAllVarsAndInfo:
	echo “Merge Everything step”
	python reorderFunctWASMooney.py
