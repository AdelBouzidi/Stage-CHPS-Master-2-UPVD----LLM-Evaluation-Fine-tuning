program pile_maker
      implicit none
      integer :: n
      integer, allocatable :: pile(:)

      read *, n
      pile = make_a_pile(n)
      print *, pile

    contains

      function make_a_pile(n) result(pile)
        implicit none
        integer, intent(in) :: n
        integer, allocatable :: pile(:)
        integer :: i

        allocate(pile(n))
        pile(1) = n
        do i = 2, n
          pile(i) = pile(i-1) + 2
        end do
      end function make_a_pile

    end program pile_maker