program starts_one_ends_demo
  implicit none
  integer :: n
  integer :: result

  ! Read input
  read(*,*) n

  ! Calculate result
  result = starts_one_ends(n)

  ! Output result
  print *, result

contains

  function starts_one_ends(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i

    if (n == 1) then
      res = 1
    else
      res = 0
      do i = 1, n
        res = res * 10 + 1
      end do
    end if

  end function starts_one_ends

end program starts_one_ends_demo