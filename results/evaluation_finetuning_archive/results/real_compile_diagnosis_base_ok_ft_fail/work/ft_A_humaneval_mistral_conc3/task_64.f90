program vowels_count
  implicit none
  character(len=*) :: input
  integer :: result

  read *, input
  result = vowels_count(input)
  print *, result

contains

  integer function vowels_count(s)
    character(len=*), intent(in) :: s
    integer :: i, len_s
    character(len=1) :: ch

    len_s = len_trim(s)
    vowels_count = 0

    do i = 1, len_s
      ch = s(i:i)
      select case (ichar(ch))
      case (97, 101, 105, 111, 117)  ! a, e, i, o, u lowercase
        vowels_count = vowels_count + 1
      case (65, 69, 73, 79, 85)  ! A, E, I, O, U uppercase
        vowels_count = vowels_count + 1
      case (121)  ! y lowercase
        if (i == len_s) then
          vowels_count = vowels_count + 1
        end if
      case (89)  ! Y uppercase
        if (i == len_s) then
          vowels_count = vowels_count + 1
        end if
      end select
    end do

  end function vowels_count

end program vowels_count