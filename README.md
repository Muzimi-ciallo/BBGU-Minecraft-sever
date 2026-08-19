这是服务于北部湾大学Minecraft多人服务器的整合包分发与增量更新仓库

增量更新逻辑
> repo/
  modpack/                ← 整合包内容（mods/config/resourcepacks/shaderpacks 都放这里）
  scripts/generate_sjmcl_update_manifest.py
  .github/workflows/update-modpack-manifest.yml
  sjmcl-update.json       ← 自动生成，玩家端就填这个的直链

  要删除某个 MOD
- 正确方式：在服务端仓库的 modpack/mods/ 里删掉那个 mod → push 重新生成 manifest。
- 玩家下次更新时，BGUMCL 会自动把它从本地实例里删除。
- 注意：如果玩家只在自己电脑上删 mod，下次更新会被重新下载回来，因为 manifest 还认为它应该存在。

推送整合包
- 点击「一键下载湾大服务器整合包」后，会自动从 Muzimi-ciallo/BBGU-Minecraft-sever 仓库的 最新 Release 下载 .mrpack 整合包（走 v4.gh-proxy.org 加速）；
- 下载完成后，自动弹出正常的整合包导入界面（和你从本地导入 .mrpack 一样的流程）。
