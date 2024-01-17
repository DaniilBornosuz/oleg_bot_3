from aiogram.fsm.state import State, StatesGroup

class FSMDialog(StatesGroup):
  user_intent = State()
  chosie_task = State()
  send_contact = State()

  async def clear(self) -> None:
    await self.set_state(state=None)
    await self.set_data({})