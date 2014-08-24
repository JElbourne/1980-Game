
`Event Example: on_key_press`

The Stack
==========

### View
if key.A: move()
if key.D: move()
if key.EXCAPE:
    leave_menu()
    return True

### Controller
if key.D: debug_on()

### Game
if key.ESCAPE: exit_game()

---

>When you push_handlers(view), you are adding all the handlers in the view object to the stack of handlers. It is added to the top as in the example above.

---

>When the pop_handlers() function is called it removes the entire top level of the stack.

---

>So the way it all works is as follows:
1. A key is pressed.
2. The top of the stack (View) uses that key
3. It then looks at the next level in the stack
4. That level uses the key
5. repeat steps 2-4 untill reach the bottom of the stack

---

>An issue may arise when you want two different stack levels to have the same event but they iterfere with one another.
To solve this and can tell the event loop to stop at any of the stack levels
by simply returning True. This will stop the stack from moving down the levels
