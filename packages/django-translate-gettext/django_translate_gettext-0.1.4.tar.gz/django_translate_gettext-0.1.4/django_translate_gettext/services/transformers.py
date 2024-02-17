import ast
from _ast import stmt


class ClassDefTransformer(ast.NodeTransformer):
    @staticmethod
    def build_new_call_node(*, constant: str) -> ast.Call:
        return ast.Call(func=ast.Name(id="_", ctx=ast.Load()), args=[ast.Constant(constant)], keywords=[])

    def generate_tuple_gettext(self, *, value: ast.Tuple | stmt) -> ast.Tuple:
        last_constant = value.elts[-1]
        if isinstance(last_constant, ast.Constant):
            value.elts[-1] = self.build_new_call_node(constant=last_constant.value)
        return value

    def generate_class_gettext(self, *, instance: ast.ClassDef | stmt) -> ast.ClassDef:
        for body in instance.body:
            if not isinstance(body, ast.Assign):
                continue

            if isinstance(body.value, ast.Constant):
                constant = body.value.value
                new_node = self.build_new_call_node(constant=constant)
                body.value = new_node

            if isinstance(body.value, ast.Tuple) and body.value.elts:
                if instance.name == "Meta":
                    continue
                body.value = self.generate_tuple_gettext(value=body.value)

        return instance

    def append_verbose_name(self, *, instance: ast.Assign | stmt) -> ast.Assign:
        constant = instance.targets[-1]
        new_node = self.build_new_call_node(constant=constant.id.title())
        instance.value.keywords.insert(0, ast.keyword(arg="verbose_name", value=new_node))

        return instance

    def generate_fk_gettext(self, *, instance: ast.Assign | stmt) -> ast.Assign:
        verbose = next((keyword for keyword in instance.value.keywords if keyword.arg == "verbose_name"), None)
        if verbose is None:
            self.append_verbose_name(instance=instance)
        else:
            constant = verbose.value
            if not isinstance(constant, ast.Constant):
                return instance
            new_node = self.build_new_call_node(constant=constant.value)
            verbose.value = new_node
        return instance

    def generate_assign_args_gettext(self, *, instance: ast.Assign | stmt) -> ast.Assign:
        if not instance.value.args and not instance.value.keywords:
            constant = instance.targets[-1]
            new_node = self.build_new_call_node(constant=constant.id.title())
            instance.value.args.append(new_node)
            return instance

        if instance.value.args:
            constant = instance.value.args[-1]
            if not isinstance(constant, ast.Constant):
                return instance
            new_node = self.build_new_call_node(constant=constant.value)
            instance.value.args[-1] = new_node
        return instance

    def generate_assign_keywords_gettext(self, *, instance: ast.Assign | stmt) -> ast.Assign:
        if instance.value.keywords:
            for keyword in instance.value.keywords:
                if keyword.arg in ("verbose_name", "help_text"):
                    constant = keyword.value
                    if not isinstance(constant, ast.Constant):
                        continue
                    new_node = self.build_new_call_node(constant=constant.value)
                    keyword.value = new_node

            verbose = next((keyword for keyword in instance.value.keywords if keyword.arg == "verbose_name"), None)
            if not instance.value.args and verbose is None:
                self.append_verbose_name(instance=instance)

        return instance

    def generate_assign_gettext(self, *, instance: ast.Assign | stmt) -> ast.Assign:
        f_keys = ("ForeignKey", "ManyToManyField", "OneToOneField")
        if hasattr(instance.value, "func") and instance.value.func.attr in f_keys:
            self.generate_fk_gettext(instance=instance)
            return instance

        if isinstance(instance.value, ast.Tuple):
            instance.value = self.generate_tuple_gettext(value=instance.value)
            return instance

        try:
            self.generate_assign_args_gettext(instance=instance)
        except AttributeError:
            return instance

        self.generate_assign_keywords_gettext(instance=instance)

        return instance

    @staticmethod
    def insert_getetxt_import(node: ast.Module) -> ast.Module:
        aliases = [body.names[-1].name for body in node.body if isinstance(body, ast.ImportFrom)]
        if "gettext_lazy" in aliases:
            return node

        counted_imports = len([
            import_node for import_node in node.body if isinstance(import_node, (ast.ImportFrom, ast.Import))
        ])

        import_node = ast.ImportFrom(
            module="django.utils.translation",
            names=[ast.alias(name="gettext_lazy", asname="_")],
            level=0,
        )
        node.body.insert(counted_imports, import_node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:  # noqa: N802
        for instance in node.body:
            match instance:
                case ast.ClassDef():
                    self.generate_class_gettext(instance=instance)
                case ast.Assign():
                    self.generate_assign_gettext(instance=instance)

        return node
