program right_angle_triangle_test
  implicit none
  integer :: a, b, c
  logical :: result

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if it's a right-angled triangle
  result = right_angle_triangle(a, b, c)

  ! Output result
  print *, result

contains

  function right_angle_triangle(a, b, c) result(res)
    implicit none
    integer, intent(in) :: a, b, c
    logical :: res
    integer :: a2, b2, c2
    integer :: max_side, other1, other2

    ! Sort the sides to identify the largest
    if (a >= b) then
      if (a >= c) then
        max_side = a
        other1 = b
        other2 = c
      else
        max_side = c
        other1 = a
        other2 = b
      end if
    else
      if (b >= c) then
        max_side = b
        other1 = a
        other2 = c
      else
        max_side = c
        other1 = b
        other2 = a
      end if
    end if

    ! Check Pythagorean theorem
    a2 = other1**2
    b2 = other2**2
    c2 = max_side**2
    res = (a2 + b2 == c2)

  end function right_angle_triangle

end program right_angle_triangle_test