from .._core import NamedModel, Message


class StripSystem(NamedModel):
    """
    Wraps a model and strips off system message (if any).
    Useful if underlying model was not trained with system message.
    """

    def __init__(self, model):
        self.model = model
        super().__init__(f"strip-system-{model.name}", self.__engine)

    def __engine(self, messages: list[Message]) -> str:
        if messages[0]["role"] == "system":
            return self.model(messages[1:])
        else:
            return self.model(messages)
