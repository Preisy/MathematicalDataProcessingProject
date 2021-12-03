from PIL import Image, ImageDraw


class PrintSalary:
    def __init__(self, common, analyze_data):
        self.salaryH = common.individual_indicator_h
        self.min_salary = min(analyze_data.history_salary)
        self.max_salary = max(analyze_data.history_salary)
        if self.max_salary - self.min_salary == 0:
            self.step_salary = 0
        else:
            self.step_salary = (self.salaryH - 5) / (self.max_salary - self.min_salary)
        self.data = analyze_data.history_salary

        self.__prepareImage(common)

        self.__drawMarks(common)

        self.__drawSalaryLines(common)

        self.__drawGraph(common)

        self.image.save("1.png", "PNG")

        size = common.image.size
        intermediate_image = Image.new("RGB", (size[0], size[1] + self.salaryH + common.dh), color="white")
        intermediate_image.paste(common.image)
        intermediate_image.paste(self.image, (0, size[1]))
        common.image = intermediate_image
        common.draw = ImageDraw.Draw(common.image)

    def __drawMarks(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        for i in range(dw + drw, w + drw + dw + 1, common.left_indent):
            self.image.draw.line((i, self.salaryH - 1, i, self.salaryH + 3), fill="black")
        # self.image.draw.line((dw + drw, self.salaryH - 1, i, self.salaryH + 3), fill="black")

    def __prepareImage(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw

        salaryH = self.salaryH

        size = common.image.size
        self.image = Image.new("RGB", (size[0], salaryH + dh), color="white")
        self.image.draw = ImageDraw.Draw(self.image)

    def __drawSalaryLines(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        salaryH = self.salaryH
        n = 5
        max_salary = self.max_salary
        min_salary = self.min_salary
        indent_px = salaryH / n
        indent_money = (max_salary - min_salary) / n
        for i in range(n + 1):
            if not (i == 0 or i == n):
                self.image.draw.line((drw + dw + 2, salaryH - i * indent_px, drw + dw + w - 2, salaryH - i * indent_px),
                               fill="grey")
            self.image.draw.text((drw + 5, salaryH - i * indent_px), str(round(min_salary + i * indent_money, 2)),
                           fill="black")


    def __drawGraph(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        min_salary = self.min_salary
        salaryH = self.salaryH
        step_salary = self.step_salary

        self.image.draw.rectangle((dw + drw, 0, w + dw + drw, salaryH), outline="black", width=2)

        left_indent = dw

        for i in range(len(self.data)):
            if i == 0:
                prev_el = self.data[i]
                left_indent += common.left_indent
                continue

            current_el = self.data[i]

            self.image.draw.line(
                (left_indent + drw - common.left_indent / 2, salaryH - 3 - step_salary * (prev_el - min_salary),
                 left_indent + drw + common.left_indent / 2, salaryH - 3 - step_salary * (current_el - min_salary)), fill="blue", width=2)

            prev_el = current_el
            left_indent += common.left_indent