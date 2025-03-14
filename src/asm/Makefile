build := build
target := boot


.PHONY:
run:
	nasm -f elf $(target).asm -o $(build)/$(target).elf
	x86_64-elf-ld -m elf_i386 $(build)/$(target).elf -o $(build)/$(target)


.PHONY:
bochs-build: clean
	nasm -f bin $(target).asm -o $(build)/$(target).bin
	bximage -q -func=create -hd=10 -imgmode=flat -sectsize=512 $(build)/$(target).img
	dd if=$(build)/$(target).bin of=$(build)/$(target).img bs=512 count=1 conv=notrunc


.PHONY:
bochs-run: bochs-build
	bochs -q -f .bochsrc


.PHONY:
bochs-dbg: bochs-build
	bochs -q -debugger -f .bochsrc


.PHONY:
vbox: clean
	nasm -f bin $(target).asm -o $(build)/$(target).bin
	dd if=$(build)/$(target).bin of=$(build)/wksp-asm/wksp-asm_1.vhd bs=512 count=1 conv=notrunc


.PHONY:
clean:
	rm -f $(build)/$(target).bin
	rm -f $(build)/$(target).img