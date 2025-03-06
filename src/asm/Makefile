build := build
target := boot


.PHONY:
all: clean
	nasm -f bin ${target}.asm -o ${build}/${target}.bin
	bximage -q -func=create -hd=10 -imgmode=flat -sectsize=512 ${build}/${target}.img
	dd if=${build}/${target}.bin of=${build}/${target}.img bs=512 count=1 conv=notrunc
	bochs -q -f .bochsrc


.PHONY:
clean:
	rm -f ${build}/${target}.bin
	rm -f ${build}/${target}.img