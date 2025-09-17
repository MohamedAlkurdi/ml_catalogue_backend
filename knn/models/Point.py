class Point:
    def __init__(self, *args,**kwargs):
        self.target = kwargs.get('target')
        self.arguments = list(args)
