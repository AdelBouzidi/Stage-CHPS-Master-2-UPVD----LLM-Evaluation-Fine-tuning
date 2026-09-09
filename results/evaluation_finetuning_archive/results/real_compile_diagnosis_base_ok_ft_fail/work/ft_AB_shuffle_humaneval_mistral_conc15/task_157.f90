program right_angle_triangle
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

  logical function right_angle_triangle(a, b, c)
    integer, intent(in) :: a, b, c
    integer :: sides(3)
    integer :: i, j

    ! Store sides in array
    sides = [a, b, c]

    ! Sort the sides (simple bubble sort)
    do i = 1, 2
      do j = i+1, 3
        if (sides(j) < sides(i)) then
          sides(i) = sides(i) + sides(j)
          sides(j) = sides(i) - sides(j)
          sides(i) = sides(i) - sides(j)
        end if
      end do
    end do

    ! Check Pythagorean theorem: a^2 + b^2 = c^2
    if (sides(1)**2 + sides(2)**2 == sides(3)**2) then
      right_angle_triangle = .true.
    else
      right_angle_triangle = .false.
    end if
  end function right_angle_triangle

end program right_angle_triangle