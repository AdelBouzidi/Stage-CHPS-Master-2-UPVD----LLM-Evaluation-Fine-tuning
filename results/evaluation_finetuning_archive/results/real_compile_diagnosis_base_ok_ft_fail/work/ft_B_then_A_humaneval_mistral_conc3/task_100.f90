program pile_program
      implicit none
      integer, parameter :: i4 = selected_int_kind(9)
      integer(i4) :: n
      integer(i4), allocatable :: pile(:)

      ! Read input
      read(*, *) n

      ! Call function
      pile = make_a_pile(n)

      ! Print output
      print *, pile
    end program pile_program