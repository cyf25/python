from student import Student

class StudentCms():
    def __init__(self):
        self.student_list = []

    @staticmethod
    def show_info():
        print("*" * 40)
        print("学生管理系统")
        print("1.添加学生")
        print("2.删除学生")
        print("3.修改学生")
        print("4.查询学生")
        print("5.显示所有学生")
        print("6.保存学生")
        print("7.退出系统")
        print("*" * 40)

    def add(self):
        name = input('请输入学生姓名：')
        age = input('请输入学生年龄：')
        gender = input('请输入学生性别：')
        mobile = input('请输入学生电话：')
        des = input('请输入学生描述：')
        student1 = Student(name, age, gender, mobile, des)
        self.student_list.append(student1)
        print(f"学生 {name} 已添加。")

    def delete(self):
        print('删除学生信息')
        name = input('请输入要删除的学生姓名：')
        for student in self.student_list:
            if student.name == name:
                self.student_list.remove(student)
                print(f"学生 {name} 已删除。")
            else:
                return print(f"没有找到学生 {name}。")

    def update(self):
        print('更新学生信息')
        name = input('请输入要更新的学生姓名：')
        for student in self.student_list:
            if student.name == name:
                student.age = input('请输入学生年龄：')
                student.gender = input('请输入学生性别：')
                student.mobile = input('请输入学生电话：')
                student.des = input('请输入学生描述：')
                print(f"学生 {name} 已更新。")
            else:
                return print(f"没有找到学生 {name}。")

    def query(self):
        print('查询学生信息')
        name = input('请输入要查询的学生姓名：')
        for student in self.student_list:
            if student.name == name:
                print(f"学生 {name} 的信息为：{student}")
            else:
                print(f"没有找到学生 {name}。")
    def show(self):
        print('显示学生信息')
        for student in self.student_list:
            print(student)

    def save(self):
        print('保存学生信息')
        try:
            with open('student.txt', 'w') as f:
                for student in self.student_list:
                    f.write(f"{student.name},{student.age},{student.gender},{student.mobile},{student.des}\n")
            print("学生信息已保存。")
        except Exception as e:
            print(f"保存学生信息时出错：{e}")
            print("学生信息未保存。")
    def exit(self):
        print('退出学生管理系统')
        user_input = input("确定要退出吗？(y/n)")
        if user_input.lower() == 'y':
            print("感谢使用学生管理系统，再见！")
            exit()
        else:
            print("取消退出。")

    def start(self):
        while True:
            self.show_info()
            user_input = input("请输入你的选择：")
            if user_input == '1':
                self.add()
            elif user_input == '2':
                self.delete()
            elif user_input == '3':
                self.update()
            elif user_input == '4':
                self.query()
            elif user_input == '5':
                self.show()
            elif user_input == '6':
                self.save()
            elif user_input == '7':
                self.exit()
            else:
                print("无效的选择，请重新输入。")

if __name__ == '__main__':
    student_cms = StudentCms()
    student_cms.start()