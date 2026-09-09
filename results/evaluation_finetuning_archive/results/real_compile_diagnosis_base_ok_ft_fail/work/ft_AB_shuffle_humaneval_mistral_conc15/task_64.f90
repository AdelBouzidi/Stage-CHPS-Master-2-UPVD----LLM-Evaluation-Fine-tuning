program vowels_count
  implicit none
  character(len=*), dimension(1) :: input
  integer :: result

  ! Read input string
  read(*, '(A)') input

  ! Count vowels
  result = vowels_count(input(1))

  ! Output result
  print *, result

contains

  integer function vowels_count(str)
    character(len=*), intent(in) :: str
    integer :: i, len_str
    character(len=1) :: ch

    len_str = len_trim(str)
    vowels_count = 0

    do i = 1, len_str
      ch = str(i:i)
      select case (ichar(ch))
      case (97, 101, 105, 111, 117)  ! a, e, i, o, u lowercase
        vowels_count = vowels_count + 1
      case (65, 69, 73, 79, 85)  ! A, E, I, O, U uppercase
        vowels_count = vowels_count + 1
      case (121)  ! y lowercase
        if (i == len_str) then
          vowels_count = vowels_count + 1
        end if
      case (89)  ! Y uppercase
        if (i == len_str) then
          vowels_count = vowels_count + 1
        end if
      end select
    end do
  end function vowels_count

end program vowels_count