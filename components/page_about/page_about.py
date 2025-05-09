﻿import subprocess
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QSizePolicy

from siui.components import (
    SiDenseVContainer,
    SiLabel,
    SiOptionCardLinear,
    SiPixLabel,
    SiPushButton,
    SiSimpleButton,
    SiTitledWidgetGroup,
)
from siui.components.page import SiPage
from siui.core import GlobalFont, Si, SiColor, SiGlobal, SiQuickEffect
from siui.gui import SiFont


class About(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setTitle("关于")

        self.titled_widget_group = SiTitledWidgetGroup(self)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        version_picture_container = SiDenseVContainer(self)
        version_picture_container.setAlignment(Qt.AlignCenter)
        version_picture_container.setFixedHeight(128 + 48)
        SiQuickEffect.applyDropShadowOn(version_picture_container, color=(28, 25, 31, 255), blur_radius=48)

        self.version_picture = SiPixLabel(self)
        self.version_picture.setFixedSize(128, 128)
        self.version_picture.setBorderRadius(0)
        self.version_picture.load("./img/logo_new.png")

        self.version_label = SiLabel(self)
        self.version_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.version_label.setFont(SiFont.tokenized(GlobalFont.M_NORMAL))
        self.version_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_D)}")
        self.version_label.setText("AI-laucher")

        version_picture_container.addWidget(self.version_picture)
        version_picture_container.addWidget(self.version_label)
        self.titled_widget_group.addWidget(version_picture_container)

        with self.titled_widget_group as group:
            group.addTitle("开源")

            self.button_to_update = SiSimpleButton(self)
            self.button_to_update.resize(32, 32)
            self.button_to_update.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_box_arrow_up_filled"))
            self.button_to_update.clicked.connect(lambda: self.update())

            self.button_to_repo = SiSimpleButton(self)
            self.button_to_repo.resize(32, 32)
            self.button_to_repo.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            self.button_to_repo.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://gitee.com/wyyyz19373765497/AI-Launcher")))

            self.option_card_update = SiOptionCardLinear(self)
            self.option_card_update.setTitle("检查更新", "检查AL-laucher的最新版本")
            self.option_card_update.load(SiGlobal.siui.iconpack.get("ic_fluent_box_arrow_up_filled"))
            self.option_card_update.addWidget(self.button_to_update)

            self.option_card_repo = SiOptionCardLinear(self)
            self.option_card_repo.setTitle("开源仓库", "在 GitHub 上查看 AI-laucher 的项目主页")
            self.option_card_repo.load(SiGlobal.siui.iconpack.get("ic_fluent_home_database_regular"))
            self.option_card_repo.addWidget(self.button_to_repo)

            self.option_card_license = SiOptionCardLinear(self)
            self.option_card_license.setTitle("开源许可证", "本项目遵循 GPLv3.0 许可证供非商业使用")
            self.option_card_license.load(SiGlobal.siui.iconpack.get("ic_fluent_certificate_regular"))

            group.addWidget(self.option_card_repo)
            group.addWidget(self.option_card_license)
            group.addWidget(self.option_card_update)

        with self.titled_widget_group as group:
            group.addTitle("版权")

            self.option_card_copyright = SiOptionCardLinear(self)
            self.option_card_copyright.setTitle("版权声明", "AI-laucher 版权所有 © 2024 by dig")
            self.option_card_copyright.load(SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))

            group.addWidget(self.option_card_copyright)

        with self.titled_widget_group as group:
            group.addTitle("第三方资源")

            self.button_to_repo2 = SiSimpleButton(self)
            self.button_to_repo2.resize(32, 32)
            self.button_to_repo2.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            self.button_to_repo2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/ChinaIceF/PyQt-SiliconUI")))


            self.option_card_icon_pack = SiOptionCardLinear(self)
            self.option_card_icon_pack.setTitle("Fluent UI 图标库", "本项目内置了 Fluent UI 图标库，Microsoft 公司保有这些图标的版权")
            self.option_card_icon_pack.load(SiGlobal.siui.iconpack.get("ic_fluent_diversity_regular"))

            self.option_card_icon_pack1 = SiOptionCardLinear(self)
            self.option_card_icon_pack1.setTitle("PyQt-SiliconUI", "本项目使用了 PyQt-SiliconUI，其原作者保留了版权")
            self.option_card_icon_pack1.load(SiGlobal.siui.iconpack.get("ic_fluent_diversity_regular"))
            self.option_card_icon_pack1.addWidget(self.button_to_repo2)

            group.addWidget(self.option_card_icon_pack1)
            group.addWidget(self.option_card_icon_pack)

        # add placeholder for better outfit
        self.titled_widget_group.addPlaceholder(64)

        # Set SiTitledWidgetGroup object as the attachment of the page's scroll area
        self.setAttachment(self.titled_widget_group)

    def update(self):
        process = subprocess.Popen('./updater.exe')
        SiGlobal.siui.windows["MAIN_WINDOW"].close()
