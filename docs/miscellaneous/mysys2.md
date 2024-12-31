# mysys2


## 参考
> - [官网](https://www.msys2.org/)


## 安装
```shell
# 1. 根据提示正常安装即可


# 2. 配置pacman
cp /etc/pacman.d/mirrorlist.msys /etc/pacman.d/mirrorlist.msys.bak
nano /etc/pacman.d/mirrorlist.msys
# 将以下内容添加到文件开头
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
# 更新数据库
pacman -Syyu


# 3. 安装yay
pacman -S base-devel
pacman -S git
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```