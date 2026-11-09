import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Particle")

clock = pygame.time.Clock()


# ==========================================
# CẤU HÌNH
# ==========================================

SO_HAT = 500

# Bán kính hút
BAN_KINH_HUT = 220

# Lực hút ban đầu
DO_HUT_CO_BAN = 0.08

# Lực hút tăng khi giữ chuột
DO_TANG_LUC = 0.003

# Lực tán loạn
DO_TAN_LOAN = 12

# Tốc độ tối đa
TOC_DO_TOI_DA = 20


# ==========================================
# TẠO HẠT
# ==========================================

particles = []

for _ in range(SO_HAT):

    particles.append({
        "x": random.uniform(0, WIDTH),
        "y": random.uniform(0, HEIGHT),

        "vx": random.uniform(-1, 1),
        "vy": random.uniform(-1, 1),

        "size": random.randint(1, 3)
    })


# ==========================================
# TRẠNG THÁI CHUỘT
# ==========================================

dang_nhan = False

thoi_gian_giu = 0

luc_hut = DO_HUT_CO_BAN


# ==========================================
# CHƯƠNG TRÌNH CHÍNH
# ==========================================

running = True

while running:

    # ======================================
    # XỬ LÝ SỰ KIỆN
    # ======================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        # ==============================
        # NHẤN CHUỘT
        # ==============================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                dang_nhan = True

                thoi_gian_giu = 0

                luc_hut = DO_HUT_CO_BAN


        # ==============================
        # BUÔNG CHUỘT
        # ==============================

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                dang_nhan = False

                mouse_x, mouse_y = pygame.mouse.get_pos()


                # ==================================
                # TÍNH LỰC TÁN LOẠN
                # ==================================

                luc_no = (
                    DO_TAN_LOAN
                    + thoi_gian_giu * 0.3
                )


                # ==================================
                # CHO CÁC HẠT BAY RANDOM
                # ==================================

                for p in particles:

                    dx = p["x"] - mouse_x
                    dy = p["y"] - mouse_y

                    distance = math.sqrt(
                        dx * dx + dy * dy
                    )


                    # Chỉ những hạt gần chuột
                    # mới bị vụ nổ tác động
                    if distance < BAN_KINH_HUT:

                        # Góc ngẫu nhiên
                        angle = random.uniform(
                            0,
                            math.pi * 2
                        )

                        direction_x = math.cos(angle)
                        direction_y = math.sin(angle)


                        # Hạt càng gần chuột
                        # càng bị bắn mạnh
                        strength = (
                            1
                            - distance / BAN_KINH_HUT
                        )


                        explosion = (
                            luc_no
                            * (0.5 + strength)
                        )


                        p["vx"] = (
                            direction_x
                            * explosion
                        )

                        p["vy"] = (
                            direction_y
                            * explosion
                        )


                    else:

                        # Hạt ở xa cũng nhận
                        # một chuyển động random nhỏ
                        p["vx"] += random.uniform(
                            -2,
                            2
                        )

                        p["vy"] += random.uniform(
                            -2,
                            2
                        )


                thoi_gian_giu = 0


    # ======================================
    # VỊ TRÍ CHUỘT
    # ======================================

    mouse_x, mouse_y = pygame.mouse.get_pos()


    # ======================================
    # ĐANG GIỮ CHUỘT
    # ======================================

    if dang_nhan:

        thoi_gian_giu += 1

        # Càng giữ → lực càng mạnh
        luc_hut = (
            DO_HUT_CO_BAN
            + thoi_gian_giu * DO_TANG_LUC
        )

        luc_hut = min(
            luc_hut,
            1.5
        )


    # ======================================
    # NỀN
    # ======================================

    screen.fill((5, 5, 15))


    # ======================================
    # XỬ LÝ HẠT
    # ======================================

    for p in particles:

        # ==================================
        # ĐANG GIỮ → HÚT VỀ CHUỘT
        # ==================================

        if dang_nhan:

            dx = mouse_x - p["x"]
            dy = mouse_y - p["y"]

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )


            if (
                distance < BAN_KINH_HUT
                and distance > 1
            ):

                direction_x = dx / distance
                direction_y = dy / distance


                # Càng gần → càng hút mạnh
                strength = (
                    1
                    - distance / BAN_KINH_HUT
                )


                p["vx"] += (
                    direction_x
                    * strength
                    * luc_hut
                )

                p["vy"] += (
                    direction_y
                    * strength
                    * luc_hut
                )


        # ==================================
        # KHÔNG NHẤN
        # → BAY RANDOM
        # ==================================

        else:

            # Chuyển động ngẫu nhiên nhẹ
            p["vx"] += random.uniform(
                -0.08,
                0.08
            )

            p["vy"] += random.uniform(
                -0.08,
                0.08
            )


        # ==================================
        # MA SÁT NHẸ
        # ==================================

        p["vx"] *= 0.985
        p["vy"] *= 0.985


        # ==================================
        # GIỚI HẠN TỐC ĐỘ
        # ==================================

        speed = math.sqrt(
            p["vx"] ** 2 +
            p["vy"] ** 2
        )


        if speed > TOC_DO_TOI_DA:

            p["vx"] = (
                p["vx"]
                / speed
                * TOC_DO_TOI_DA
            )

            p["vy"] = (
                p["vy"]
                / speed
                * TOC_DO_TOI_DA
            )


        # ==================================
        # CẬP NHẬT VỊ TRÍ
        # ==================================

        p["x"] += p["vx"]
        p["y"] += p["vy"]


        # ==================================
        # ĐI QUA BIÊN → XUẤT HIỆN PHÍA ĐỐI DIỆN
        # ==================================

        if p["x"] < 0:
            p["x"] = WIDTH

        elif p["x"] > WIDTH:
            p["x"] = 0


        if p["y"] < 0:
            p["y"] = HEIGHT

        elif p["y"] > HEIGHT:
            p["y"] = 0


        # ==================================
        # VẼ HẠT
        # ==================================

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                int(p["x"]),
                int(p["y"])
            ),
            p["size"]
        )


    pygame.display.flip()

    clock.tick(60)


pygame.quit()