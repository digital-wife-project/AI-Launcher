
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from siui.components import SiPixLabel
from siui.components.option_card import SiOptionCardLinear, SiOptionCardPlane
from siui.components.page import SiPage
from siui.components.slider import SiSliderH
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiLineEdit,
    SiLongPressButton,
    SiPushButton,
    SiSimpleButton,
    SiSwitch,
)
from siui.core import GlobalFont, Si, SiColor, SiGlobal, SiQuickEffect, GlobalFontSize
from siui.gui import SiFont

from .components.themed_option_card import ThemedOptionCardPlane


class ExampleHomepage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 滚动区域
        self.scroll_container = SiTitledWidgetGroup(self)

        # 整个顶部
        self.head_area = SiLabel(self)
        self.head_area.setFixedHeight(450)

        # 创建背景底图和渐变
        self.background_image = SiPixLabel(self.head_area)
        self.background_image.setFixedSize(1366, 300)
        self.background_image.setBorderRadius(6)
        self.background_image.load("./img/homepage_background.png")

        self.background_fading_transition = SiLabel(self.head_area)
        self.background_fading_transition.setGeometry(0, 100, 0, 200)
        self.background_fading_transition.setStyleSheet(
            """
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 {}, stop:1 {})
            """.format(SiGlobal.siui.colors["INTERFACE_BG_B"],
                       SiColor.trans(SiGlobal.siui.colors["INTERFACE_BG_B"], 0))
        )

        # 创建大标题和副标题
        self.title = SiLabel(self.head_area)
        self.title.setGeometry(64, 0, 500, 128)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setText("AI-laucher")
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.title.setFont(SiFont.tokenized(GlobalFont.XL_MEDIUM))

        self.subtitle = SiLabel(self.head_area)
        self.subtitle.setGeometry(64, 72, 500, 48)
        self.subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.subtitle.setText("A powerful and artistic all in one solution for AI.")
        self.subtitle.setStyleSheet("color: {}".format(SiColor.trans(SiGlobal.siui.colors["TEXT_A"], 0.9)))
        self.subtitle.setFont(SiFont.tokenized(GlobalFont.S_MEDIUM))

        # 创建一个水平容器
        self.container_for_cards = SiDenseHContainer(self.head_area)
        self.container_for_cards.move(0, 130)
        self.container_for_cards.setFixedHeight(310)
        self.container_for_cards.setAlignment(Qt.AlignCenter)
        self.container_for_cards.setSpacing(32)

        # 添加卡片
        self.option_card_project = ThemedOptionCardPlane(self)
        self.option_card_project.setTitle("GitHub Repo")
        self.option_card_project.setFixedSize(218, 270)
        self.option_card_project.setThemeColor("#855198")
        self.option_card_project.setDescription(
            "check All AI laucher on GitHub to get the latest release, report errors, provide suggestions and more.")  # noqa: E501
        self.option_card_project.setURL("https://github.com")

        self.option_card_example = ThemedOptionCardPlane(self)
        self.option_card_example.setTitle("Examples")
        self.option_card_example.setFixedSize(218, 270)
        self.option_card_example.setThemeColor("#7573aa")
        self.option_card_example.setDescription("Check examples to understand how to use AL to develop your first work.")  # noqa: E501
        self.option_card_example.setURL("Examples are Coming soon...")

        # 添加到水平容器
        self.container_for_cards.addPlaceholder(64 - 32)
        self.container_for_cards.addWidget(self.option_card_project)
        self.container_for_cards.addWidget(self.option_card_example)

        # 添加到滚动区域容器
        self.scroll_container.addWidget(self.head_area)

        # SiQuickEffect.applyDropShadowOn(self.container_for_cards, color=(0, 0, 0, 80), blur_radius=48)

        # 下方区域标签
        self.body_area = SiLabel(self)
        self.body_area.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.body_area.resized.connect(lambda _: self.scroll_container.adjustSize())

        # 下面的 titledWidgetGroups
        self.titled_widget_group = SiTitledWidgetGroup(self.body_area)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.titled_widget_group.resized.connect(lambda size: self.body_area.setFixedHeight(size[1]))
        self.titled_widget_group.move(64, 0)

        self.titled_widget_group.setSpacing(16)
        self.titled_widget_group.addPlaceholder(64)

        # 添加到滚动区域容器
        self.body_area.setFixedHeight(self.titled_widget_group.height())
        self.scroll_container.addWidget(self.body_area)

        # 添加到页面
        self.setAttachment(self.scroll_container)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        self.body_area.setFixedWidth(w)
        self.background_image.setFixedWidth(w)
        self.titled_widget_group.setFixedWidth(min(w - 128, 900))
        self.background_fading_transition.setFixedWidth(w)
