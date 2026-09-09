program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input from stdin
  read(*,*) x
  read(*,*) y

  ! Call the function
  result = choose_num(x, y)

  ! Print output to stdout
  print *, result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res
    integer :: i

    res = -1
    do i = y, x, -1
      if (mod(i, 2) == 0) then
        res = i
        exit
      end if
    end do
  end function choose_num

end program choose_num_demo