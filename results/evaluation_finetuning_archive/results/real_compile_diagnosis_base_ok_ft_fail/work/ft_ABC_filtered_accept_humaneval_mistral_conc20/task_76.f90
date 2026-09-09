program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read(*,*) x
  read(*,*) n

  ! Call the function
  result = is_simple_power(x, n)

  ! Output result
  print *, result

contains

  function is_simple_power(x, n) result(res)
    implicit none
    integer, intent(in) :: x, n
    logical :: res
    integer :: i

    if (n == 0) then
      res = .false.
      return
    end if

    if (x == 0) then
      res = .false.
      return
    end if

    if (x < 0) then
      if (mod(x, n) /= 0) then
        res = .false.
        return
      end if
    end if

    res = .true.
    do i = 1, 30
      if (x == n**i) then
        exit
      end if
      if (x < n**i) then
        res = .false.
        exit
      end if
    end do

  end function is_simple_power

end program is_simple_power_demo