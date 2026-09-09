program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read *, x
  n = 2  ! Using 2 as the base for power check

  ! Check if x is a simple power of n
  result = is_simple_power(x, n)

  ! Output result
  print *, result

contains

  logical function is_simple_power(x, n)
    implicit none
    integer, intent(in) :: x, n
    integer :: i

    if (x <= 0) then
      is_simple_power = .false.
    else if (n <= 1) then
      is_simple_power = .false.
    else
      is_simple_power = .true.
      do i = 1, 30
        if (n**i == x) then
          exit
        else if (n**i > x) then
          is_simple_power = .false.
          exit
        end if
      end do
    end if
  end function is_simple_power

end program is_simple_power_demo