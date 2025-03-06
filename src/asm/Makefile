build := ${shell pwd}/build
target := boot


.PHONY:
boot: boot.asm
	rm "${build}/${target}.*"
	nasm -f bin "${target}.asm" -o "${build}/${target}.bin"
	bximage -q -func=create -hd=10 -imgmode=flat -sectsize=512 "${build}/${target}.bin"
	dd -if="${build}/${target}.bin" -of="${build}/${target}.img" bs=512 count=1 conv=notrunc
	bochs -q -f .bochsrc
