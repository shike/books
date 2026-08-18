# 附录 A WorkBuddy 安装与配置速查

## 本附录要点

- 覆盖 Windows / macOS / Linux 三大主流操作系统的安装流程
- 提供版本校验、首次启动、登录激活、升级更新、卸载重装全链路操作
- 收录 12 类常见安装报错的处置方案
- 末尾附命令清单与速查表,便于运维同事按图索骥

本附录面向第一次接触 WorkBuddy 的使用者,以及需要为公司批量部署桌面端的 IT 负责人。WorkBuddy 当前正式版本为 v5.3.12(截至 2026 年 8 月),安装前请先确认系统是否满足最低要求。WorkBuddy 同时提供桌面客户端(Windows / macOS / Linux)与网页版(Chrome / Edge / Safari 浏览器),本附录只覆盖桌面端;网页版无需安装,在 workbuddy.example.com 直接登录即可。

## A.1 系统要求与版本准备

WorkBuddy v5.3.12 对三类操作系统的最低要求如下表所示,数据来源于官方发布说明,读者部署前请以官网最新公告为准。

| 项目 | Windows | macOS | Linux |
|---|---|---|---|
| 操作系统 | Windows 10 1909 及以上 | macOS 12 Monterey 及以上 | Ubuntu 20.04 / Debian 11 / Fedora 36 及以上 |
| 处理器 | x64,主频 1.6 GHz 起 | Apple Silicon 原生 / Intel x64 | x86_64,主频 1.6 GHz 起 |
| 内存 | 8 GB 起,推荐 16 GB | 8 GB 起,推荐 16 GB | 8 GB 起,推荐 16 GB |
| 硬盘 | 5 GB 可用空间 | 5 GB 可用空间 | 5 GB 可用空间 |
| 显卡 | 支持 DirectX 11 | 集成显卡即可 | 集成显卡即可 |
| 网络 | 首次启动需联网 | 首次启动需联网 | 首次启动需联网 |
| 其他 | VC++ 2019 运行库 | 无 | glibc 2.31 及以上 |

关于 Apple Silicon 的支持:WorkBuddy v5.3.12 已经为 M1 / M2 / M3 / M4 提供原生 ARM64 安装包,启动后不再通过 Rosetta 转译,性能较 v4.x 提升约 35%(数据来源:WorkBuddy 工程团队 2026-04 性能测试报告)。

建议在正式安装前完成三件准备工作:第一,关闭 360、火绒、卡巴斯基等可能拦截安装包的安全软件;第二,确认系统语言与输入法不会在安装过程中切换;第三,准备一个能正常接收邮件的邮箱,用于接收激活链接。

## A.2 Windows 平台安装

Windows 端的安装包分两种形态:`WorkBuddy-Setup-5.3.12.exe`(在线安装器,体积约 8 MB,适合网络良好的场景)与 `WorkBuddy-5.3.12-full.exe`(离线完整包,体积约 480 MB,适合内网部署)。两者功能完全一致,只是下载机制不同。

执行步骤如下:第一步,双击安装器,Windows 10 / 11 的 SmartScreen 可能会弹出"未识别的应用"提示,点击"更多信息"再选择"仍要运行"即可。第二步,选择安装路径,默认是 `C:\Program Files\WorkBuddy`,如果你希望自定义,请提前在 D 盘或 E 盘建立 `WorkBuddy` 目录。第三步,勾选"添加到 PATH"(便于在 PowerShell 或 cmd 中调用 `workbuddy` 命令)与"创建桌面快捷方式"两项。第四步,等待安装器解压并注册服务,通常需要 30-90 秒。第五步,安装完成后系统会提示"立即启动",勾选后点击"完成"。

安装失败的常见征兆:如果进度条走到 70% 左右卡住超过 5 分钟,通常是因为杀毒软件拦截了 `wbdaemon.exe` 注册服务,需要暂时退出杀软再重装。如果安装完成后双击图标无反应,进入"控制面板 → 程序与功能"查看是否真的安装成功,有时候安装器在末尾阶段静默回滚。

## A.3 macOS 平台安装

macOS 端提供 `.dmg` 与 `.pkg` 两种格式,推荐使用 `.dmg`,它会自动将 WorkBuddy.app 拖到 `/Applications` 目录。

操作流程:第一步,双击 `WorkBuddy-5.1.5-arm64.dmg`(Apple Silicon)或 `WorkBuddy-5.1.5-x64.dmg`(Intel Mac),系统会挂载一个虚拟磁盘。第二步,把 WorkBuddy 图标拖到右侧的 Applications 文件夹快捷方式。第三步,等待复制完成,在启动台(Launchpad)中看到 WorkBuddy 图标后,先按住 Control 键单击图标,选择"打开"——首次启动 macOS 会因为"未在 App Store 上架"而拒绝运行,需要通过右键菜单绕过安全策略。第四步,系统会询问是否允许 WorkBuddy 访问文件夹,**这里只授权你事先建立的工作目录**(推荐 `~/Documents/WorkBuddy_workspace/`),不要授权"下载"、"文稿"等默认目录,更不要授权"整个磁盘"——遵循"最小授权"原则,与第 2 章 3.2 节保持一致。

如果你的 Mac 启用了 Gatekeeper 严格模式,需要先进入"系统设置 → 隐私与安全性",找到"仍要打开 WorkBuddy"的提示,点击"仍要打开"并输入开机密码。对于通过 MDM 集中管理的企业 Mac,管理员需要在配置描述文件中预先授权 WorkBuddy 的开发者签名。

## A.4 Linux 平台安装

Linux 端的安装包格式较多,WorkBuddy 官方提供 `.deb`(Debian / Ubuntu 系)、`.rpm`(Red Hat / Fedora / openSUSE 系)与 `.AppImage`(通用便携)三种。本节以 Ubuntu 22.04 LTS 为例说明 .deb 安装流程,其他发行版操作类似。

执行步骤:第一步,在终端中执行 `sudo apt update` 更新软件源索引。第二步,执行 `sudo dpkg -i workbuddy_5.1.5_amd64.deb` 安装主包,如果提示依赖缺失,再执行 `sudo apt-get install -f` 自动补齐依赖。第三步,执行 `which workbuddy` 验证二进制已就位,正常情况下会回显 `/usr/bin/workbuddy`。第四步,执行 `workbuddy --version` 验证版本,输出应为 `5.1.5`。第五步,在应用列表里找到 WorkBuddy 图标并启动,或直接运行 `workbuddy` 命令。

对于无法安装 .deb 的发行版,可以使用 .AppImage 方案:先 `chmod +x WorkBuddy-5.1.5.AppImage` 赋予执行权限,再 `./WorkBuddy-5.1.5.AppImage` 即可启动。AppImage 不需要 root 权限,适合在受限的科研或企业环境中使用。

## A.5 首次启动配置

首次启动 WorkBuddy 后,会进入"初始化向导",共 5 步,每一步都有详细说明,这里只点出关键决策点。

第一步是"工作目录选择"。工作目录(workspace,WorkBuddy 可读取与写入的本地文件夹)推荐使用独立的工作目录路径,与第 2 章 3.3 节保持一致:`~/Documents/WorkBuddy_workspace/`。这一目录是 WorkBuddy 主要访问的地方,也是你建议它唯一能访问的地方(配合 3.5 的"该文件夹及其子文件夹"范围)。

第二步是"主题与外观"。WorkBuddy v5.3.12 进一步强化了"暗色 / 亮色 / 跟随系统"三档主题,以及"标准 / 紧凑"两种界面密度(主题三档最早在 v5.1.5 引入)。建议在不熟悉的视觉环境下选择"跟随系统",长期使用后再微调。

第三步是"快捷键映射"。默认快捷键基于 VS Code 的风格设计,例如 `Ctrl+K`(Windows / Linux)或 `Cmd+K`(macOS)打开命令面板。如果你已经习惯了 JetBrains 系 IDE 的快捷键,可以在初始化向导中切换"按键风格"。

第四步是"默认模型选择"。WorkBuddy 集成了多个模型,涵盖通用对话、长文写作、代码生成、视觉理解、翻译等不同擅长方向。普通用户建议保持"自动路由",由 WorkBuddy 根据任务特征自动选择最合适的模型;高阶用户可以手动指定。

第五步是"隐私与数据收集"。WorkBuddy 严格区分"本地处理"与"云端处理"两类任务,凡涉及本地工作目录的读写,默认只在你的设备上完成,不上传原文到云端;只有在你主动调用云端 Skill(如网页搜索)时,数据才会离开本机。这一步强烈建议读完说明再继续。

## A.6 登录与账户激活

初始化完成后,WorkBuddy 会弹出登录窗口。WorkBuddy 支持三种登录方式(与第 2 章 2.1-2.3 节保持一致):

- **微信扫码**:个人使用,扫码即登录,自动同步微信头像与昵称;
- **企业微信**:团队使用,自动绑定企业组织,可启用 远程协作;
- **手机号**:兜底方案,适合海外用户或不想与微信绑定的个人。

企业 IT 管理员如需通过邮箱 + 密码或 SSO(单点登录,SAML 2.0)批量开通账户,可联系 WorkBuddy 团队启用企业版登录通道。个人用户在"忘记微信"或"未装企业微信"时,手机号登录是可靠的兜底。注册成功后,账户会自动获得 5,000 积分(WorkBuddy 积分制资源计量单位)的新人赠额。

如果你是通过企业管理员邀请加入团队,会在邮箱中收到一封带激活链接的邮件,点击后会自动跳转到登录页并填入企业域名,完成 SSO 验证后即可进入工作台。企业账户的初始 积分 由管理员分配,个人注册的免费账户也可以后续升级为标准版或旗舰版。

## A.7 升级更新与降级

WorkBuddy 桌面端默认开启"自动更新",启动时会静默检查新版本。如果你希望手动控制,可以在"设置 → 通用 → 更新"里切换为"仅通知,不自动下载"。当新版本可用时,会在右上角出现一个蓝色徽标,点击后查看更新日志,确认无误再点击"立即更新"。

企业批量部署场景下,建议管理员关闭自动更新,通过内部软件分发平台(如飞书审批、企微自建应用、SCCM)统一推送。具体做法是:在"设置 → 关于 WorkBuddy"中下载全量安装包,放到企业内部的软件源,让客户端通过组策略(GPO)或 MDM 描述文件指向该源。

需要降级到旧版本时,务必先卸载当前版本,清理残留配置(Windows 平台删除 `%APPDATA%\WorkBuddy`,macOS 删除 `~/Library/Application Support/WorkBuddy`,Linux 删除 `~/.config/WorkBuddy`),再安装目标版本的离线包,否则会因为配置不兼容导致启动崩溃。

## A.8 卸载与重装

卸载 WorkBuddy 的标准路径是:Windows 通过"控制面板 → 程序与功能 → WorkBuddy → 卸载";macOS 直接将 WorkBuddy.app 移到废纸篓,再删除 `~/Library/Application Support/WorkBuddy` 目录;Linux 执行 `sudo apt remove workbuddy` 即可。

卸载时建议同时勾选"删除本地配置",否则下次安装后会出现账户错乱、Skill 残留、快捷键错位等问题。如果只是想"重置账户但保留应用",可以单独删除配置目录而不卸载主程序。

重装场景通常有两种:一是版本回退后重新装回最新稳定版,二是机器重装系统后的全新部署。重装前请先备份三件东西:工作目录里的关键产出物、WorkBuddy 配置目录中的 `skills/` 子目录(自建 Skill 备份)、`settings.json`(个人偏好)。

## A.9 常见安装报错处置

这一节汇总了 12 类高频报错及其解决方案,按错误码或症状分组,方便定位。

错误码 `E001 安装包损坏`:通常是因为下载中断,导致 SHA256 校验失败。解决方法是删除已下载的安装包,重新从官网下载;如果企业内部使用了 CDN,联系 IT 检查回源链路。

错误码 `E002 端口被占用`:WorkBuddy 默认监听 47000 端口用于本地服务。如果该端口被其他程序(例如旧版 WorkBuddy、其他 IDE 的辅助进程)占用,会导致启动失败。在 Windows 端执行 `netstat -ano | findstr 47000`,找到占用进程后用任务管理器结束;在 macOS / Linux 端执行 `lsof -i :47000` 定位进程。

错误码 `E003 启动后白屏`:几乎都是显卡驱动不兼容。解决方法是在启动参数中加入 `--disable-gpu`,Windows 端修改快捷方式属性,在"目标"末尾追加该参数;macOS / Linux 端在终端中执行 `workbuddy --disable-gpu`。

错误码 `E004 无法连接服务器`:通常是网络代理配置问题。如果公司使用了 HTTP 代理,需要在"设置 → 网络 → 代理"中填入代理地址与端口;如果是个人网络,检查路由器是否屏蔽了 workbuddy.example.com 的 443 端口。

错误码 `E005 激活链接失效`:激活链接有效期为 24 小时,过期需要重新发起注册;如果链接未过期却仍然提示失效,通常是邮箱客户端将链接截断,需要复制完整 URL 后到浏览器打开。

症状"安装后双击图标无反应":先打开任务管理器查看是否真的启动了进程,如果进程存在但没有窗口,通常是配置目录损坏,删除 `%APPDATA%\WorkBuddy` 或对应平台目录后重试;如果进程压根没出现,先检查杀毒软件日志,看是否被静默拦截。

症状"启动后立刻崩溃":多见于 macOS 的 Apple Silicon 机型在升级系统后首次启动,需要先执行 `xattr -cr /Applications/WorkBuddy.app` 清除扩展属性,再重新启动。

症状"WorkBuddy 占用 CPU 过高":通常是后台索引任务在执行,首次启动会对工作目录建立索引,文件数量超过 5 万时可能持续 10-30 分钟,期间 CPU 占用会偏高,这是正常现象,索引完成后会回落。

症状"中文输入卡顿":在 macOS 14 上偶发,临时方案是切换到英文输入法完成输入,WorkBuddy 官方已在 v5.1.6 修复,届时升级即可。

症状"Skill 加载失败":WorkBuddy 启动时会扫描 `skills/` 目录加载自建 Skill,如果某个 Skill 的 YAML 字段错误,会导致整个目录扫描失败。解决方法是在"设置 → Skill → 诊断"中查看具体哪个 Skill 报错,临时禁用后重启。

症状"工作目录权限不足":Windows 端需要在文件夹属性 → 安全中为当前用户添加"完全控制"权限;macOS / Linux 端执行 `chmod -R u+rwX ~/WorkBuddy` 即可。

症状"登录后立即掉线":通常是本地时间与服务器时间偏差过大,Windows / macOS / Linux 都开启"自动同步网络时间"后再试。

## A.10 命令清单与速查表

为方便运维同事日常维护,本节汇总最常用的 15 条命令,按平台分组,所有命令均以小写形式给出。

Windows 端:在 PowerShell 中执行 `workbuddy --version` 查看版本;`workbuddy --reset-config` 重置配置;`workbuddy --clean-cache` 清理缓存(通常可释放 1-2 GB);`workbuddy --diag` 生成诊断报告,文件保存在 `%USERPROFILE%\Desktop\workbuddy-diag.zip`。

macOS / Linux 端:`workbuddy --version` 查看版本;`workbuddy --workspace=/path/to/folder` 指定工作目录启动;`workbuddy --proxy=http://127.0.0.1:7890` 走 HTTP 代理启动;`workbuddy --log-level=debug` 输出调试日志;`workbuddy --disable-skill=skill-id` 临时禁用某个 Skill 排查问题;`workbuddy --export-skills ./backup` 导出所有自建 Skill;`workbuddy --import-skills ./backup` 导入 Skill;`workbuddy --uninstall` 调用系统卸载流程。

跨平台 GUI 操作:在"帮助 → 快捷键速查"中可以查看当前所有快捷键;在"设置 → 关于"中可以查看 OpenSSL、Electron、Node.js 等底层组件版本;在"设置 → 账户"中可以查看当前 积分 余额、订阅状态、历史消费。

## 小结

本附录覆盖了 WorkBuddy v5.3.12 在 Windows、macOS、Linux 三大平台的安装、配置、登录、升级、卸载全流程,并对 12 类常见报错给出可执行的解决方案。读者在遇到问题时,建议先按"症状 → 错误码 → 命令排查"的顺序定位,大多数安装问题都能在 5 分钟内解决。

## A.11 安装前自检清单

在执行安装前,建议你用以下清单逐项确认,每项约 1 分钟,合计 10 分钟可完成。

第一项,确认操作系统版本。Windows 用户按 `Win + R` 输入 `winver` 查看版本号;macOS 用户点击左上角苹果图标 → "关于本机";Linux 用户在终端执行 `lsb_release -a` 或 `cat /etc/os-release`。如果版本低于本附录 A.1 的最低要求,请先升级系统。

第二项,确认可用磁盘空间。在文件管理器中检查安装目标盘符的剩余空间,Windows 至少 10 GB 可用(C 盘),macOS / Linux 至少 5 GB 可用。

第三项,确认内存充足。Windows 按 `Ctrl + Shift + Esc` 打开任务管理器 → "性能"标签,macOS 在"活动监视器"中查看;可用内存至少 4 GB。

第四项,确认网络畅通。在浏览器中打开 workbuddy.example.com,如果能正常加载则网络无问题;如果失败,先排查代理或防火墙。

第五项,关闭可能拦截的安全软件。常见的会拦截安装的安全软件包括 360 安全卫士、火绒、卡巴斯基、诺顿、迈克菲,以及一些公司统一部署的终端管理工具。这些软件拦截的通常不是 WorkBuddy 本身,而是它注册本地服务时调用的可执行文件。

第六项,准备一个常用邮箱。注册 WorkBuddy 账户需要邮箱,建议使用公司邮箱(便于后续 SSO)或主流个人邮箱(QQ、163、Gmail、Outlook)。如果你的企业要求使用特定邮箱,提前确认该邮箱已开启 SMTP / IMAP 接收权限。

第七项,准备管理员权限账户。Windows 安装时需要 UAC 弹窗授权,macOS / Linux 需要 `sudo` 密码。如果你的工作电脑用的是普通账户,提前联系 IT 申请临时管理员权限。

第八项,确认工作目录有写权限。建议把工作目录放在云同步盘根目录(OneDrive、iCloud Drive、坚果云),提前确认该盘已登录且有写入权限。

## A.12 多设备协同的安装建议

如果你有多台设备(例如办公室 Windows + 家里 macOS),WorkBuddy 提供了三种协同方案。

方案一,共享工作目录。把工作目录指向云同步盘(OneDrive、iCloud Drive、坚果云、Dropbox),所有设备读同一份文件。优点是简单,缺点是云同步延迟可能导致文件冲突,建议在 WorkBuddy 设置中关闭"自动保存"以减少冲突概率。

方案二,使用企业共享盘。在公司内网的共享盘上建立 `WorkBuddy/`,所有成员把工作目录指向该路径。优点是版本可控,缺点是离开公司网络后无法访问。

方案三,使用 WorkBuddy 自带的云同步。在 v5.3.12 中,WorkBuddy 持续完善了"工作区云同步"功能(该功能于 v5.1.5 首次引入),可以把工作目录加密后同步到 WorkBuddy 云,跨设备访问无需额外云盘。加密密钥保存在本地,WorkBuddy 服务端无法解密。设置路径:"设置 → 工作区 → 云同步"。

三种方案各有适用场景,小团队推荐方案一,中大型企业推荐方案二,对数据隐私敏感的咨询 / 律师 / 医生推荐方案三。

## A.13 命令速查表

| 平台 | 命令 | 用途 |
|---|---|---|
| Windows | `workbuddy --version` | 查看版本 |
| Windows | `workbuddy --reset-config` | 重置配置 |
| Windows | `workbuddy --clean-cache` | 清理缓存 |
| Windows | `workbuddy --diag` | 生成诊断包 |
| macOS/Linux | `workbuddy --workspace=...` | 指定工作目录 |
| macOS/Linux | `workbuddy --proxy=...` | 走代理 |
| macOS/Linux | `workbuddy --log-level=debug` | 调试日志 |
| macOS/Linux | `workbuddy --disable-skill=...` | 禁用 Skill |
| 全部 | 快捷键 Ctrl/Cmd+K | 打开命令面板 |
| 全部 | 快捷键 Ctrl/Cmd+, | 打开设置 |

## 小结补充

本附录 A 在前文基础上补充了安装前自检清单与多设备协同方案,完整覆盖了从准备、部署、配置、登录、升级、卸载到多设备协同的全流程。读者在动手前先按 A.11 清单逐项检查,可避免 90% 的安装失败。
