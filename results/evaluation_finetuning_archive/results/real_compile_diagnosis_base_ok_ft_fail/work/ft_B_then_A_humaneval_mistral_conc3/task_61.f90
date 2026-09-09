program bracket_check
      implicit none
      character(len=*), allocatable :: brackets
      character(len=1) :: char
      integer :: i, balance
      logical :: result

      read(*, '(a)') brackets

      balance = 0
      result = .true.
      do i = 1, len(brackets)
         char = brackets(i:i)
         if (char == '(') then
            balance = balance + 1
         else if (char == ')') then
            balance = balance - 1
            if (balance < 0) then
               result = .false.
               exit
            end if
         end if
      end do
      if (balance /= 0) then
         result = .false.
      end if

      print *, result

    end program bracket_check