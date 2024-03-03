from .models import Student, Product, Group, UserProductAccess


def distribute_users_after_started(self, product: Product) -> None:
    # Getting all Groups By Product
    groups = Group.objects.filter(product=product).order_by('students_count')

    # Getting list of accessed Users
    users = UserProductAccess.objects.filter(
        product=product).values_list('user', flat=True)

    # Calculating
    min_group_size = product.min_group_size
    max_group_size = product.max_group_size

    users_count = users.count()
    groups_count = groups.count()

    target_group_size = users_count // groups_count
    remainder = users_count % groups_count

    user_index = 0
    for group in groups:
        group.students.set(users[user_index:user_index + target_group_size])
        user_index += target_group_size

        if remainder > 0:
            group.students.add(users[user_index])
            user_index += 1
            remainder -= 1

        group.students.set(group.students.all()[:max_group_size])

        if group.students.count() < min_group_size:
            needed_users = min_group_size - group.students.count()
            additional_users = users[user_index:user_index + needed_users]
            group.students.add(*additional_users)
            user_index += needed_users


def distribute_users_before_started(product: Product) -> None:
    # Getting all Groups
    groups = product.group_set.all()

    # Getting Count and total students
    total_groups = groups.count()
    total_students = product.creator.groups.count()

    # Calculating
    avg_students_per_group = total_students // total_groups
    remainder_students = total_students % total_groups

    for group in groups:
        group_students_count = group.students.count()
        if group_students_count < group.max_users:
            if remainder_students > 0 and group_students_count < avg_students_per_group + 1:
                group.students.add(product.creator)
                remainder_students -= 1
            elif group_students_count < avg_students_per_group:
                group.students.add(product.creator)


def user_has_access_to_product(product_id: int, user: Student) -> bool:
    try:
        product = Product.objects.get(id=product_id)
        user_product_access = UserProductAccess.objects.filter(
            product=product, user=user).exists()
        return user_product_access
    except Product.DoesNotExist:
        return False
